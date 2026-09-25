from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Document
from .services.processor import process_document

logger = get_task_logger(__name__)

@shared_task(
        bind=True,
        autoretry_for=(Exception,),
        retry_backoff=True,
        retry_kwargs={"max_retries": 3},
)
def process_document_task(self, document_id):
    document = Document.objects.get(id=document_id)

    logger.info(
        "Starting document processing: document_id=%s",
        document_id
    )

    try:
        document.status = "processing"
        document.save(
            update_fields=["status", "updated_at"]
        )

        process_document(document)

        logger.info(
            "Document processed successfully: document_id=%s",
            document_id
        )

        return {
            "document_id": document_id,
            "status": "processed",
        }

    except Exception:

        logger.exception(
            "Document processing failed: document_id=%s",
            document_id
        )

        document.status = "failed"
        document.save(
            update_fields=["status", "updated_at"]
        )
        raise