from django.urls import path
from .views import (ChatView, ChatHistoryView, ChatMessageDataView)

urlpatterns = [
    path("", ChatView.as_view(), name="chat"),
    path("history/", ChatHistoryView.as_view(), name="chat-history"),
    path("<int:pk>/", ChatMessageDataView.as_view(), name="chat-detail"),
]
