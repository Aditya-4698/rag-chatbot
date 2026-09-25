from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(APITestCase):

    def test_register_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "aditya",
                "email": "aditya@example.com",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="aditya"
            ).exists()
        )

        self.assertIn(
            "token",
            response.data,
        )


    def test_login_user(self):

        User.objects.create_user(
            username="aditya",
            password="strongpass123",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "aditya",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "token",
            response.data,
        )


    def test_invalid_login(self):

        User.objects.create_user(
            username="aditya",
            password="strongpass123",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "aditya",
                "password": "wrongpassword",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_me_requires_authentication(self):

        response = self.client.get(
            "/api/auth/me/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_me_returns_current_user(self):

        user = User.objects.create_user(
            username="aditya",
            password="strongpass123",
        )

        token = Token.objects.create(
            user=user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.get(
            "/api/auth/me/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["username"],
            "aditya",
        )