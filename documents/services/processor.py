import logging

from django.db import transaction

from documents.models import Document, DocumentChunk
from .chunker import chunk_text
from .embeddings import generate_embedding
from .extractor import extract_pdf_pages
from .vector_store import add_chunk, delete_document_chunks


logger = logging.getLogger(__name__)


def process_document(document):
    """
    Extract, clean, chunk and save a document's content.
    """

    document.status = "processing"
    document.save(update_fields=["status"])

    logger.info(
        "Document processing started: document_id=%s",
        document.id,
    )

    try:
        logger.info(
            "Extracting PDF: document_id=%s",
            document.id,
        )

        pages = extract_pdf_pages(
            document.file
        )

        logger.info(
            "PDF extraction completed: document_id=%s, pages=%s",
            document.id,
            len(pages),
        )

        if not pages:
            raise ValueError(
                "No pages found in PDF."
            )

        has_text = any(
            page["text"].strip()
            for page in pages
        )

        if not has_text:
            raise ValueError(
                "No extractable text found in PDF."
            )

        with transaction.atomic():

            logger.info(
                "Removing old chunks and vectors: document_id=%s",
                document.id,
            )

            delete_document_chunks(
                document.id
            )

            # Remove old chunks if the document
            # is being processed again.
            DocumentChunk.objects.filter(
                document=document
            ).delete()

            chunk_index = 0
            total_chunks = 0

            for page in pages:

                chunks = chunk_text(
                    page["text"]
                )

                for content in chunks:

                    chunk = DocumentChunk.objects.create(
                        document=document,
                        content=content,
                        chunk_index=chunk_index,
                        page_number=page["page_number"],
                        metadata={
                            "page": page["page_number"],
                            "source": document.title,
                        },
                    )

                    embedding = generate_embedding(
                        content
                    )

                    add_chunk(
                        chunk_id=chunk.id,
                        content=content,
                        embedding=embedding,
                        metadata={
                            "user_id": document.user_id,
                            "document_id": document.id,
                            "page": page["page_number"],
                            "chunk_index": chunk_index,
                        },
                    )

                    chunk_index += 1
                    total_chunks += 1

            logger.info(
                "Chunks created: document_id=%s, chunks=%s",
                document.id,
                total_chunks,
            )

        document.status = "processed"
        document.save(update_fields=["status"])

        logger.info(
            "Vector processing completed: document_id=%s",
            document.id,
        )

    except Exception:
        logger.exception(
            "Document processing failed: document_id=%s",
            document.id,
        )

        document.status = "failed"
        document.save(update_fields=["status"])

        raise