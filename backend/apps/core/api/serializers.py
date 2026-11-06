from rest_framework import serializers

from apps.core.models import ImpactStat, Partner, SiteSettings, SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="get_platform_display", read_only=True)

    class Meta:
        model = SocialLink
        fields = ["platform", "label", "url"]


class PartnerSerializer(serializers.ModelSerializer):
    kind_label = serializers.CharField(source="get_kind_display", read_only=True)

    class Meta:
        model = Partner
        fields = [
            "id", "name", "slug", "kind", "kind_label",
            "logo", "website", "description", "is_featured",
        ]


class ImpactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStat
        fields = ["id", "label", "value", "suffix", "icon", "description"]


class SiteSettingsSerializer(serializers.ModelSerializer):
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        exclude = ["id", "created_at", "updated_at"]

    def get_social_links(self, obj):
        qs = SocialLink.objects.published()
        return SocialLinkSerializer(qs, many=True, context=self.context).data
