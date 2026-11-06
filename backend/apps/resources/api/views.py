from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.resources.models import Publication

from .serializers import PublicationSerializer


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.published().select_related("programme")
    serializer_class = PublicationSerializer
    lookup_field = "slug"
    filterset_fields = ["kind", "year", "is_featured", "programme__slug"]
    search_fields = ["title", "summary"]
    ordering_fields = ["published_date", "year", "title"]

    @action(detail=True, methods=["post"], url_path="register-download")
    def register_download(self, request, slug=None):
        """Count a download without blocking the file itself."""
        publication = self.get_object()
        Publication.objects.filter(pk=publication.pk).update(
            download_count=F("download_count") + 1
        )
        return Response({"status": "recorded"})
