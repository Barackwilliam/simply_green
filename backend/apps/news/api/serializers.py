from rest_framework import serializers

from apps.news.models import Category, Event, EventRegistration, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "colour"]


class PostListSerializer(serializers.ModelSerializer):
    kind_label = serializers.CharField(source="get_kind_display", read_only=True)
    category = CategorySerializer(read_only=True)
    author_display = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "kind", "kind_label", "title", "slug", "excerpt",
            "featured_image", "featured_image_alt", "category", "tags",
            "author_display", "published_at", "reading_minutes", "is_featured",
        ]

    def get_author_display(self, obj):
        if obj.author:
            return obj.author.full_name
        return obj.author_name

    def get_tags(self, obj):
        return [t.name for t in obj.tags.all()]


class PostDetailSerializer(PostListSerializer):
    programme_title = serializers.CharField(
        source="programme.title", read_only=True, default=""
    )
    programme_slug = serializers.CharField(
        source="programme.slug", read_only=True, default=""
    )

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + [
            "body", "featured_image_credit", "audio_url", "audio_file",
            "programme_title", "programme_slug", "view_count",
            "meta_title", "meta_description", "og_image", "noindex",
        ]


class EventListSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    registration_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "title", "slug", "summary", "featured_image",
            "start_datetime", "end_datetime", "status", "status_label",
            "venue", "is_online", "registration_enabled", "registration_open",
            "is_featured",
        ]


class EventDetailSerializer(EventListSerializer):
    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + [
            "body", "address", "map_embed_url", "online_url",
            "registration_deadline", "capacity",
            "meta_title", "meta_description", "og_image", "noindex",
        ]


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = [
            "id", "event", "full_name", "email", "phone",
            "organisation", "notes",
        ]

    def validate(self, attrs):
        event = attrs["event"]
        if not event.registration_open:
            raise serializers.ValidationError(
                "Registration for this event is closed."
            )
        return attrs
