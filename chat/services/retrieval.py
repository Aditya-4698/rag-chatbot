import logging

from config.exceptions import VectorStoreError
from documents.services.embeddings import generate_embedding
from documents.services.vector_store import search_chunks

logger = logging.getLogger(__name__)


def retrieve_relevant_chunks(
    question,
    user_id,
    n_results=5,
):
    try:
        query_embedding = generate_embedding(question)

        results = search_chunks(
            query_embedding=query_embedding,
            user_id=user_id,
            n_results=n_results,
        )

    except Exception as exc:
        logger.exception(
            "Retrieval failed: user_id=%s",
            user_id,
        )

        raise VectorStoreError(
            "Document search is temporarily unavailable."
        ) from exc

    documents = results.get(
        "documents",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    distances = results.get(
        "distances",
        [[]],
    )[0]

    retrieved_chunks = []

    for index, content in enumerate(documents):
        retrieved_chunks.append({
            "content": content,
            "metadata": metadatas[index],
            "distance": distances[index],
        })

    return retrieved_chunks