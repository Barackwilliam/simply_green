from rest_framework import serializers

from apps.about.models import CoreValue, Objective, PartnerReason, TeamMember


class CoreValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreValue
        fields = ["id", "title", "description", "icon"]


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ["id", "text"]


class PartnerReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerReason
        fields = ["id", "title", "description", "icon"]


class TeamMemberSerializer(serializers.ModelSerializer):
    group_label = serializers.CharField(source="get_group_display", read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            "id", "full_name", "slug", "role", "group", "group_label",
            "photo", "short_bio", "bio", "email", "linkedin", "x_handle",
        ]
