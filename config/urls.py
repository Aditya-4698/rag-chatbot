from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, health_check

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", home, name="home"),
    path("health/", health_check, name="health"),

    path(
        "api/auth/",
        include("accounts.urls"),
    ),

    path(
        "api/documents/",
        include("documents.urls"),
    ),

    path(

        "api/chat/",
        include("chat.urls")
    )
    
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )