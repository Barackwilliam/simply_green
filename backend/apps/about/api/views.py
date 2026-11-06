from rest_framework import viewsets

from apps.about.models import CoreValue, Objective, PartnerReason, TeamMember

from .serializers import (
    CoreValueSerializer,
    ObjectiveSerializer,
    PartnerReasonSerializer,
    TeamMemberSerializer,
)


class CoreValueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CoreValue.objects.published()
    serializer_class = CoreValueSerializer
    pagination_class = None


class ObjectiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Objective.objects.published()
    serializer_class = ObjectiveSerializer
    pagination_class = None


class PartnerReasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PartnerReason.objects.published()
    serializer_class = PartnerReasonSerializer
    pagination_class = None


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.published()
    serializer_class = TeamMemberSerializer
    lookup_field = "slug"
    filterset_fields = ["group"]
    pagination_class = None
