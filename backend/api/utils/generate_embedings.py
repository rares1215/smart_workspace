from sentence_transformers import SentenceTransformer

# Load model ONCE when Django starts (fast & efficient)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

def generate_embedding(text: str):
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()  # convert to Python list for pgvector


def generate_embedding_for_chunks(chunks: list[str]):
    vectors = []
    for chunk in chunks:
        vector = generate_embedding(chunk)
        vectors.append(vector)
    return vectors
