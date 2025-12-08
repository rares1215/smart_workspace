from ..utils.generate_embedings import generate_embedding
from ..models import DocumentEmbedding
from django.db.models.functions import Cast
from pgvector.django import CosineDistance
from django.db.models import FloatField
from ..utils.analyze_text_with_llm import ask_groq


def rag_answer(document_id: str, query: str):
    #Create embedding for query
    query_vector = generate_embedding(query)

    # 2. Search top relevant chunks using cosine similarity
    results = (
        DocumentEmbedding.objects
        .filter(document_id=document_id)
        .annotate(distance=CosineDistance("embedding", query_vector))
        .order_by("distance")[:5]  # take top 5 chunks
    )

    # 3. Build context from retrieved chunks
    context = "\n\n".join(chunk.chunk_text for chunk in results)

    # 4. Prepare prompt
    prompt = f"""
    You are an AI assistant. Answer the user's question using ONLY the context below.
    If the answer cannot be found in the context, say "The document does not contain enough information."

    --- CONTEXT START ---
    {context}
    --- CONTEXT END ---

    User question: {query}
    """

    answer = ask_groq(prompt)

    return {
        "query": query,
        "context_used": context,
        "prompt": prompt,
        "answer": answer,
    }
