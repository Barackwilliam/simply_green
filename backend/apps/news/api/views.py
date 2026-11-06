from django.db.models import F
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.news.models import Category, Event, EventRegistration, Post

from .serializers import (
    CategorySerializer,
    EventDetailSerializer,
    EventListSerializer,
    EventRegistrationSerializer,
    PostDetailSerializer,
    PostListSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.published()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = None


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_fields = ["kind", "category__slug", "is_featured", "programme__slug"]
    search_fields = ["title", "excerpt", "body"]
    ordering_fields = ["published_at", "title", "view_count"]

    def get_queryset(self):
        return (
            Post.objects.published()
            .select_related("category", "author", "programme")
            .prefetch_related("tags")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(view_count=F("view_count") + 1)
        return Response(self.get_serializer(instance).data)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    filterset_fields = ["status", "is_featured", "programme__slug"]
    search_fields = ["title", "summary", "venue"]
    ordering_fields = ["start_datetime", "title"]

    def get_queryset(self):
        qs = Event.objects.published()
        when = self.request.query_params.get("when")
        if when == "upcoming":
            qs = qs.filter(start_datetime__gte=timezone.now()).order_by(
                "start_datetime"
            )
        elif when == "past":
            qs = qs.filter(start_datetime__lt=timezone.now())
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventDetailSerializer
        return EventListSerializer


class EventRegistrationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Write-only: the public can register, but cannot read the attendee list."""

    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
