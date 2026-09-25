from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.throttling import ScopedRateThrottle

from .models import ChatMessage
from .serializers import (
    ChatMessageSerializer,
    ChatRequestSerializer,
    )
from .services.rag import generate_answer

from django.shortcuts import render

# Create your views here.

class ChatView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "chat"

    def post(self, request):

        serializer = ChatRequestSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        question = serializer.validated_data[
            "question"
        ]

        result = generate_answer(
            question=question,
            user_id=request.user.id,
        )

        chat_message = ChatMessage.objects.create(
            user=request.user,
            question=question,
            answer=result["answer"],
        )

        return Response(
            {
                "id": chat_message.id,
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"],
                "created_at": chat_message.created_at,
            },
            status=status.HTTP_200_OK
        )


class ChatHistoryView(
    generics.ListAPIView
):

    serializer_class = ChatMessageSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class ChatMessageDataView(
    generics.RetrieveDestroyAPIView
):

    serializer_class = ChatMessageSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            user = self.request.user
        )