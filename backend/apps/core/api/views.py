from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import ImpactStat, Partner, SiteSettings

from .serializers import (
    ImpactStatSerializer,
    PartnerSerializer,
    SiteSettingsSerializer,
)


class SiteSettingsView(APIView):
    """Site-wide identity, contact details and SEO defaults."""

    def get(self, request):
        settings_obj = SiteSettings.load()
        return Response(
            SiteSettingsSerializer(settings_obj, context={"request": request}).data
        )


class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.published()
    serializer_class = PartnerSerializer
    lookup_field = "slug"
    filterset_fields = ["kind", "is_featured"]
    search_fields = ["name", "description"]


class ImpactStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ImpactStat.objects.published()
    serializer_class = ImpactStatSerializer
    pagination_class = None
