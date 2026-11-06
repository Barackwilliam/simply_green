from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    EventRegistrationViewSet,
    EventViewSet,
    PostViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("posts", PostViewSet, basename="post")
router.register("events", EventViewSet, basename="event")
router.register(
    "event-registrations", EventRegistrationViewSet, basename="event-registration"
)

urlpatterns = [path("", include(router.urls))]
