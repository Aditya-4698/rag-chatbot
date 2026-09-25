from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    chunk_count = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "file_type",
            "status",
            "created_at",
            "updated_at",
            "chunk_count",
        ]

        read_only_fields = [
            "id",
            "file_type",
            "status",
            "created_at",
            "updated_at",
            "chunk_count",
        ]

    def get_chunk_count(self, obj):
        return obj.chunks.count()


    def validate_file(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only pdf file are supported."
            )

        max_size = 10 * 1024 * 1024 

        if value.size > max_size:

            raise serializers.ValidationError(
                "PDF file size must be less than 10 MB."
            )
        
        return value