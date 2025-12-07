from groq import Groq
from decouple import config

client  = Groq(
    api_key=config('GROQ_API_KEY')
)



def generate_embedding(text):
    response = client.embeddings.create(
        model="llama-3.1-8b-embedding",
        input=text
    )
    return response.data[0].embedding


def generate_embedding_for_chunks(chunks:list[str]):
    vectors = []
    for chunk in chunks:
        vector = generate_embedding(chunk)
        vectors.append(vector)
    return vectors