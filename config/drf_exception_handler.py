import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from .exceptions import (
    AIServiceError,
    VectorStoreError,
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(
        exc,
        context,
    )

    if isinstance(exc, AIServiceError):
        logger.error(
            "AI service error",
            exc_info=True,
        )

        return Response(
            {
                "error": str(exc),
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    if isinstance(exc, VectorStoreError):
        logger.error(
            "Vector store error",
            exc_info=True,
        )

        return Response(
            {
                "error": str(exc),
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    if response is not None:
        return response

    logger.exception(
        "Unhandled application exception",
        exc_info=True,
    )

    return Response(
        {
            "error": "An unexpected error occurred."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )