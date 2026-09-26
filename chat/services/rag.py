import logging
import os

from google import genai

from config.exceptions import AIServiceError
from .prompts import build_rag_prompt
from .retrieval import retrieve_relevant_chunks


logger = logging.getLogger(__name__)


LLM_MODEL = "gemini-3.5-flash-lite"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
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
            "document_id": metadata.get("document_id"),
            "page": metadata.get("page"),
            "chunk_index": metadata.get("chunk_index"),
        })

    context = "\n\n".join(context_parts)

    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    if client is None:
        raise AIServiceError(
            "Gemini API key is not configured."
        )

    try:
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
        )

    except Exception as exc:
        logger.exception(
            "Gemini LLM request failed: user_id=%s",
            user_id,
        )

        raise AIServiceError(
            "AI service is temporarily unavailable."
        ) from exc

    return {
        "answer": response.text,
        "sources": sources,
    }