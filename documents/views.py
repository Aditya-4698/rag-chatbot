from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer
# from .services.processor import process_document
from .tasks import process_document_task
from .services.vector_store import delete_document_chunks

from django.shortcuts import render

# Create your views here.

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


    def perform_create(self, serializer):
        file = self.request.FILES.get("file")

        document = serializer.save(
            user=self.request.user,
            file_type=file.name.split(".")[-1].lower(),
        )

        process_document_task.delay(document.id)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        )


    def perform_destroy(self, instance):

        # Remove vectors from ChromaDB first
        delete_document_chunks(instance.id)

        # Then delete the Django object
        instance.delete()