from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CoreValueViewSet,
    ObjectiveViewSet,
    PartnerReasonViewSet,
    TeamMemberViewSet,
)

router = DefaultRouter()
router.register("core-values", CoreValueViewSet, basename="core-value")
router.register("objectives", ObjectiveViewSet, basename="objective")
router.register("partner-reasons", PartnerReasonViewSet, basename="partner-reason")
router.register("team", TeamMemberViewSet, basename="team-member")

urlpatterns = [path("", include(router.urls))]
