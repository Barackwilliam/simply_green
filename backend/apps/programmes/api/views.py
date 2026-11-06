from rest_framework import viewsets

from apps.programmes.models import FocusArea, Programme

from .serializers import (
    FocusAreaDetailSerializer,
    FocusAreaSerializer,
    ProgrammeDetailSerializer,
    ProgrammeListSerializer,
)


class FocusAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FocusArea.objects.published()
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FocusAreaDetailSerializer
        return FocusAreaSerializer


class ProgrammeViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_fields = ["status", "is_featured", "focus_areas__slug"]
    search_fields = ["title", "subtitle", "summary", "location", "beneficiaries"]
    ordering_fields = ["start_date", "title", "display_order"]

    def get_queryset(self):
        qs = Programme.objects.published().prefetch_related("focus_areas")
        if self.action == "retrieve":
            qs = qs.prefetch_related("outcomes", "images", "partners")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProgrammeDetailSerializer
        return ProgrammeListSerializer
