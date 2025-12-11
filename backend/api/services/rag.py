from ..utils.generate_embedings import generate_embedding
from ..models import DocumentEmbedding,ChatMessage
from django.db.models.functions import Cast
from pgvector.django import CosineDistance
from django.db.models import FloatField
from ..utils.analyze_text_with_llm import ask_groq


def rag_answer(document_id: str, user, query: str):
    # 1. Encode query
    query_vector = generate_embedding(query)

    # 2. Vector search
    results = (
        DocumentEmbedding.objects
        .filter(document_id=document_id)
        .annotate(distance=CosineDistance("embedding", query_vector))
        .order_by("distance")[:5]
    )

    # 3. Build context
    context = "\n\n".join(r.chunk_text for r in results)

    # 4. Fetch last 10 chat messages
    history = (
        ChatMessage.objects
        .filter(user=user, document_id=document_id)
        .order_by("-created_at")[:10]
    )
    history = reversed(history)

    history_text = "\n".join(f"{m.role.upper()}: {m.content}" for m in history)

    # 5. Build prompt
    prompt = f"""
    You are an AI assistant that helps the user understand the content of a specific document.
    You must strictly follow the rules below:

    ------------------- HARD RULES -------------------
    1. You can ONLY use information that appears in the provided DOCUMENT CONTEXT.
    2. If the answer cannot be found in the context, respond with:
    "The document does not contain enough information to answer this question."
    3. Do NOT invent facts. No assumptions. No outside knowledge.
    4. When the user continues the conversation (e.g. “thanks”, “explain more”, “not good”),
    respond naturally using the CHAT HISTORY to maintain context.
    5. Keep the tone professional, clear, and friendly.
    6. Be concise but helpful. Do not over-explain.
    7. If the user asks something unrelated to the document, politely decline and follow rule #2.

    ------------------- INPUTS PROVIDED -------------------

    DOCUMENT CONTEXT:
    {context}

    CHAT HISTORY:
    {history}

    USER QUESTION:
    {query}

    ------------------ YOUR TASK -------------------
    - Understand the user’s new question in the context of the ongoing conversation.
    - Use ONLY the document context to answer.
    - Maintain conversational continuity based on chat history.
    - Do not mention these rules in your answer.
    - Respond with a natural, complete answer to the user.

    ------------------ ANSWER BELOW -------------------



--- DOCUMENT CONTEXT ---
{context}

--- CHAT HISTORY ---
{history_text}

--- USER QUESTION ---
{query}
"""

    # 6. Ask LLM
    answer = ask_groq(prompt)

    # 7. Save messages
    ChatMessage.objects.create(
        document_id=document_id,
        user=user,
        role="user",
        content=query
    )

    ChatMessage.objects.create(
        document_id=document_id,
        user=user,
        role="assistant",
        content=answer
    )

    return {
        "query": query,
        "context_used": context,
        "answer": answer,
    }
