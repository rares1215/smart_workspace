from sentence_transformers import SentenceTransformer
from django.core.cache import cache
import hashlib
# Load model ONCE when Django starts (fast & efficient)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

CACHE_TIMEOUT = 60 * 60 * 24 ## expire date for items in cache

def generate_embedding(text: str):
    hash_text = hashlib.sha256(text.encode('utf-8')).hexdigest()

    key = f"embedding:{hash_text}"
    cached_vector = cache.get(key)
    if cached_vector:
        print("CACHED HIT!")
        return cached_vector
    
    vector = model.encode(text,convert_to_numpy=True).tolist()
    cache.set(key,vector,CACHE_TIMEOUT)

    return vector


def generate_embedding_for_chunks(chunks: list[str]):
    vectors = []
    for chunk in chunks:
        vector = generate_embedding(chunk)
        vectors.append(vector)
    return vectors
