from django.contrib.auth.models import User
from django.db import models


class EvaluationCase(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="evaluation_cases",
    )

    question = models.TextField()

    expected_answer = models.TextField(
        blank=True
    )

    expected_keywords = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question[:80]



class EvaluationResult(models.Model):

    evaluation_case = models.ForeignKey(
        EvaluationCase,
        on_delete=models.CASCADE,
        related_name="results",
    )

    generated_answer = models.TextField()

    retrieved_chunks = models.PositiveIntegerField(
        default=0
    )

    keyword_score = models.FloatField(
        default=0
    )

    retrieval_score = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Evaluation {self.evaluation_case_id}"
        )