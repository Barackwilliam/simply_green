from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ImpactStatViewSet, PartnerViewSet, SiteSettingsView

router = DefaultRouter()
router.register("partners", PartnerViewSet, basename="partner")
router.register("impact-stats", ImpactStatViewSet, basename="impact-stat")

urlpatterns = [
    path("site-settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("", include(router.urls)),
]
