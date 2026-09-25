import redis
import requests

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from config.celery import app as celery_app


def home(request):
    return render(request, "index.html")


def health_check(request):
    checks = {}

    # Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        checks["database"] = "ok"

    except Exception:
        checks["database"] = "error"

    # Redis
    try:
        redis_client = redis.Redis.from_url(
            settings.CELERY_BROKER_URL
        )

        redis_client.ping()

        checks["redis"] = "ok"

    except Exception:
        checks["redis"] = "error"

    # Ollama
    try:
        response = requests.get(
            f"{settings.OLLAMA_BASE_URL}/api/tags",
            timeout=3,
        )

        checks["ollama"] = (
            "ok" if response.ok else "error"
        )

    except Exception:
        checks["ollama"] = "error"

    # Celery
    try:
        workers = celery_app.control.inspect().ping()

        checks["celery"] = (
            "ok" if workers else "error"
        )

    except Exception:
        checks["celery"] = "error"

    overall_status = (
        "ok"
        if all(status == "ok" for status in checks.values())
        else "error"
    )

    return JsonResponse(
        {
            "status": overall_status,
            "checks": checks,
        },
        status=200 if overall_status == "ok" else 503,
    )