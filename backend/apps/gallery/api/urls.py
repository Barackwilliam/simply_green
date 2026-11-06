from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, VideoViewSet

router = DefaultRouter()
router.register("albums", AlbumViewSet, basename="album")
router.register("videos", VideoViewSet, basename="video")

urlpatterns = [path("", include(router.urls))]
