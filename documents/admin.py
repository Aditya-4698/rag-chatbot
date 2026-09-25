from django.contrib import admin
from .models import Document, DocumentChunk
# Register your models here.

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "file_type",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "file_type",
        "created_at",   
    )

    search_filter = (
        "title",
        "user__username",
    )

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "chunk_index",
        "page_number",
        "created_at",
    )

    search_filters = (
        "document_title",
        "content",
    )