import chromadb
from django.conf import settings


CHROMA_PATH = settings.BASE_DIR / "vectorstore"


def get_collection():
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    return client.get_or_create_collection(
        name="document_chunks"
    )


def add_chunk(
        chunk_id,
        content,
        embedding,
        metadata,
):
    """
    Store a document chunk in ChromaDB.
    """

    collection = get_collection()

    collection.add(
        ids=[str(chunk_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def delete_document_chunks(document_id):

    collection = get_collection()

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

    collection = get_collection()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "user_id": user_id
        },
    )


def get_all_chunks():

    collection = get_collection()

    return collection.get(
        include=["documents", "metadatas"]
    )