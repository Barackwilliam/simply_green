from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FocusAreaViewSet, ProgrammeViewSet

router = DefaultRouter()
router.register("focus-areas", FocusAreaViewSet, basename="focus-area")
router.register("", ProgrammeViewSet, basename="programme")

urlpatterns = [path("", include(router.urls))]
