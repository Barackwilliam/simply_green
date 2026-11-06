from rest_framework import serializers

from apps.core.api.serializers import PartnerSerializer
from apps.programmes.models import (
    FocusArea,
    Programme,
    ProgrammeImage,
    ProgrammeOutcome,
)


class FocusAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusArea
        fields = [
            "id", "title", "slug", "summary", "icon", "image", "accent_colour",
        ]


class FocusAreaDetailSerializer(FocusAreaSerializer):
    class Meta(FocusAreaSerializer.Meta):
        fields = FocusAreaSerializer.Meta.fields + [
            "body", "meta_title", "meta_description", "og_image", "noindex",
        ]


class ProgrammeOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeOutcome
        fields = ["id", "label", "value"]


class ProgrammeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeImage
        fields = ["id", "image", "caption", "alt_text"]


class ProgrammeListSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    focus_areas = FocusAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Programme
        fields = [
            "id", "title", "slug", "subtitle", "status", "status_label",
            "summary", "featured_image", "location", "region", "district",
            "beneficiaries", "beneficiary_count", "start_date", "end_date",
            "focus_areas", "is_featured",
        ]


class ProgrammeDetailSerializer(ProgrammeListSerializer):
    outcomes = ProgrammeOutcomeSerializer(many=True, read_only=True)
    images = ProgrammeImageSerializer(many=True, read_only=True)
    partners = PartnerSerializer(many=True, read_only=True)

    class Meta(ProgrammeListSerializer.Meta):
        fields = ProgrammeListSerializer.Meta.fields + [
            "body", "outcomes", "images", "partners",
            "meta_title", "meta_description", "og_image", "noindex",
        ]
