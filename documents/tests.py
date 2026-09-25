from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Document

class DocumentAPITests(APITestCase):

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


    def create_pdf(slef, name="test.pdf"):

        return SimpleUploadedFile(
            name=name,
            content=b"%PDF-test-content",
            content_type="application/pdf",
        )


    def test_document_list_requires_authentication(self):

        response = self.client.get(
            "/api/documents/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


    def test_user_can_see_own_documents(self):

        Document.objects.create(
            user=self.user1,
            title="User 1 PDF",
            file=self.create_pdf(),
            file_type="pdf",
        )

        Document.objects.create(
            user=self.user2,
            title="User 2 PDF",
            file=self.create_pdf("user2.pdf"),
            file_type="pdf",
        )

        self.authenticate_user1()

        response = self.client.get(
            "/api/documents/"
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
            response.data[0]["title"],
            "User 1 PDF",
        )


    def test_user_cannot_access_other_users_document(self):

        document = Document.objects.create(
            user=self.user2,
            title="Private PDF",
            file=self.create_pdf(),
            file_type="pdf",
        )

        self.authenticate_user1()

        response = self.client.get(
            f"/api/documents/{document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_user_cannot_delete_other_users_document(self):

        document = Document.objects.create(
            user=self.user2,
            title="Private PDF",
            file= self.create_pdf(),
            file_type="pdf",
        )

        self.authenticate_user1()

        response = self.client.delete(
            f"/api/documents/{document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Document.objects.filter(
                id=document.id
            ).exists()
        )

    def test_only_pdf_files_are_allowed(self):

        self.authenticate_user1()

        file = SimpleUploadedFile(
            "notes.txt",
            b"hello",
            content_type="text/plain",
        )

        response = self.client.post(
            "/api/documents/",
            {
                "title": "Notes",
                "file": file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_large_pdf_is_rejected(self):

        self.authenticate_user1()

        large_content = b"x" *(
            10 * 1024 * 1024 + 1
        )

        file = SimpleUploadedFile(
            "large.pdf",
            large_content,
            content_type="application/pdf",
        )

        response = self.client.post(
            "/api/documents/",
            {
                "title": "Large PDF",
                "file": file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )