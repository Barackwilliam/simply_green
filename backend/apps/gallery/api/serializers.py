from rest_framework import serializers

from apps.gallery.models import Album, Photo, Video


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image", "caption", "alt_text", "credit"]


class AlbumListSerializer(serializers.ModelSerializer):
    photo_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Album
        fields = [
            "id", "title", "slug", "description", "cover_image",
            "date", "location", "photo_count", "is_featured",
        ]


class AlbumDetailSerializer(AlbumListSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta(AlbumListSerializer.Meta):
        fields = AlbumListSerializer.Meta.fields + ["photos"]


class VideoSerializer(serializers.ModelSerializer):
    source_label = serializers.CharField(source="get_source_display", read_only=True)

    class Meta:
        model = Video
        fields = [
            "id", "title", "slug", "description", "source", "source_label",
            "video_url", "video_file", "thumbnail", "duration_label",
            "date", "is_featured",
        ]
