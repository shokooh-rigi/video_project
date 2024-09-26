from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import consumers
from .views import CategoryViewSet, VideoViewSet, ChunkedUploadView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-chunk/', ChunkedUploadView.as_view(), name='chunked-upload'),
]

websocket_urlpatterns = [
    re_path(r'ws/upload_progress/$', consumers.UploadProgressConsumer.as_asgi()),
]
