from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ChatMessage

        fields = [
            "id",
            "question",
            "answer",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "answer",
            "created_at",
        ]


class ChatRequestSerializer(
    serializers.Serializer
):

    question = serializers.CharField(
        max_length=2000,
        allow_blank=False,
        trim_whitespace=True
    )