import os
import ollama

EMBEDDING_MODEL = "nomic-embed-text"

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

client = ollama.Client(
    host=OLLAMA_HOST
)


def generate_embedding(text):
    response = client.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]