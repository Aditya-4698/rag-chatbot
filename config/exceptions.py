class AIServiceError(Exception):
    """Raised when the AI service is unavailabe."""


class VectorStoreError(Exception):
    """Raised when the vector store operation fails."""


class DocumentProcessingError(Exception):
    """Raised when document processing fails."""