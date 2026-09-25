import logging
import os

import ollama

from config.exceptions import AIServiceError
from .prompts import build_rag_prompt
from .retrieval import retrieve_relevant_chunks


logger = logging.getLogger(__name__)


LLM_MODEL = "llama3.2"

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

client = ollama.Client(
    host=OLLAMA_HOST
)


def generate_answer(question, user_id, n_results=5):
    """
    Generate an answer using retrieved document context.
    """

    chunks = retrieve_relevant_chunks(
        question=question,
        user_id=user_id,
        n_results=n_results,
    )

    if not chunks:
        return {
            "answer": (
                "I could not find relevant information "
                "in your documents."
            ),
            "sources": [],
        }

    context_parts = []
    sources = []

    for chunk in chunks:
        context_parts.append(
            chunk["content"]
        )

        metadata = chunk["metadata"]

        sources.append({
            "document_id": metadata.get(
                "document_id"
            ),
            "page": metadata.get(
                "page"
            ),
            "chunk_index": metadata.get(
                "chunk_index"
            ),
        })

    context = "\n\n".join(
        context_parts
    )

    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    try:
        response = client.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    except Exception as exc:
        logger.exception(
            "Ollama LLM request failed: user_id=%s",
            user_id,
        )

        raise AIServiceError(
            "AI service is temporarily unavailable."
        ) from exc

    return {
        "answer": response["message"]["content"],
        "sources": sources,
    }