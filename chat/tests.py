from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import ChatMessage


class ChatAPITests(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username="user1",
            password="strongpass123",
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="strongpass123",
        )

        self.token1 = Token.objects.create(
            user=self.user1
        )

        self.token2 = Token.objects.create(
            user=self.user2
        )


    def authenticate_user1(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token1.key}"
        )


    def authenticate_user2(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token2.key}"
        )


    def test_chat_requires_authentication(self):

        response = self.client.post(
            "/api/chat/",
            {
                "question": "What is Django?"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_empty_question_is_rejected(self):

        self.authenticate_user1()

        response = self.client.post(
            "/api/chat/",
            {
                "question": ""
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )



    @patch(
    "chat.views.generate_answer"
    )
    def test_chat_returns_rag_answer(
        self,
        mock_generate_answer,
    ):

        mock_generate_answer.return_value = {
            "answer": "Django is a Python web framework.",
            "sources": [
                {
                    "document_id": 1,
                    "page": 2,
                    "chunk_index": 4,
                }
            ],
        }


        self.authenticate_user1()


        response = self.client.post(
            "/api/chat/",
            {
                "question": "What is Django?"
            },
            format="json",
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            response.data["answer"],
            "Django is a Python web framework.",
        )


        self.assertEqual(
            len(response.data["sources"]),
            1,
        )


        mock_generate_answer.assert_called_once_with(
            question="What is Django?",
            user_id=self.user1.id,
        )

    def test_chat_history_is_user_isolated(self):

        ChatMessage.objects.create(
            user=self.user1,
            question="Question from user 1",
            answer="Answer 1",
        )

        ChatMessage.objects.create(
            user=self.user2,
            question="Question from user 2",
            answer="Answer 2",
        )


        self.authenticate_user1()


        response = self.client.get(
            "/api/chat/history/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


        self.assertEqual(
            len(response.data),
            1,
        )


        self.assertEqual(
            response.data[0]["question"],
            "Question from user 1",
        )


    def test_user_cannot_access_other_users_chat(self):

        message = ChatMessage.objects.create(
            user=self.user2,
            question="Private question",
            answer="Private answer",
        )


        self.authenticate_user1()


        response = self.client.get(
            f"/api/chat/{message.id}/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )