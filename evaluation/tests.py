from django.contrib.auth.models import User
from django.test import TestCase

from .services.evaluator import (
    calculate_keyword_score,
    calculate_retrieval_score,
)


class EvaluationTests(TestCase):

    def test_keyword_score(self):

        score = calculate_keyword_score(
            answer="Django is a Python web framework.",
            expected_keywords=[
                "python",
                "web framework",
            ],
        )

        self.assertEqual(
            score,
            1.0,
        )


    def test_partial_keyword_score(self):

        score = calculate_keyword_score(
            answer="Django is a framework.",
            expected_keywords=[
                "python",
                "web framework",
            ],
        )

        self.assertEqual(
            score,
            0.0,
        )


    def test_empty_keywords(self):

        score = calculate_keyword_score(
            answer="Django is a framework.",
            expected_keywords=[],
        )

        self.assertEqual(
            score,
            0.0,
        )