from rest_framework import serializers

from apps.resources.models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    kind_label = serializers.CharField(source="get_kind_display", read_only=True)
    download_url = serializers.CharField(read_only=True)
    programme_title = serializers.CharField(
        source="programme.title", read_only=True, default=""
    )

    class Meta:
        model = Publication
        fields = [
            "id", "title", "slug", "kind", "kind_label", "summary",
            "download_url", "cover_image", "published_date", "year",
            "page_count", "file_size_label", "programme", "programme_title",
            "is_featured", "download_count",
        ]
