from rest_framework import viewsets

from apps.gallery.models import Album, Video

from .serializers import AlbumDetailSerializer, AlbumListSerializer, VideoSerializer


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_fields = ["is_featured", "programme__slug", "event__slug"]
    search_fields = ["title", "description", "location"]

    def get_queryset(self):
        qs = Album.objects.published()
        if self.action == "retrieve":
            qs = qs.prefetch_related("photos")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AlbumDetailSerializer
        return AlbumListSerializer


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.published()
    serializer_class = VideoSerializer
    lookup_field = "slug"
    filterset_fields = ["source", "is_featured", "programme__slug"]
    search_fields = ["title", "description"]
