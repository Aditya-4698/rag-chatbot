import chromadb
from django.conf import settings

CHROMA_PATH = settings.BASE_DIR / "vectorstore"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="document_chunks"
)

def add_chunk(
        chunk_id,
        content,
        embedding,
        metadata,
):
    """
    Store a document chunk in Chromadb.
    """

    collection.add(
        ids=[str(chunk_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata],
    )

def delete_document_chunks(document_id):
    collection.delete(
        where={
            "document_id": document_id,
        }
    )

def search_chunks(
        query_embedding,
        user_id,
        n_results=5,
):

    """
    Search only the current user's document chunks.
    """

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "user_id": user_id
        },
    )


def get_all_chunks():
    return collection.get(
        include=["documents", "metadatas"]
    )