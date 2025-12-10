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
You are an AI assistant answering questions about a user-uploaded document.
Use ONLY the document context + the chat history.

If the answer is not in the context, respond:
"The document does not contain enough information."

You may use the chat history to maintain conversational continuity(if the client says thank you you respond with "My pleasure" etc.)


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
