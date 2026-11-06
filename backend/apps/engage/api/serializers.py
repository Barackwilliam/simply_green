from rest_framework import serializers

from apps.engage.models import (
    ContactMessage,
    DonationMethod,
    DonationPledge,
    NewsletterSubscriber,
    PartnerEnquiry,
    VolunteerApplication,
)


class HoneypotMixin(serializers.Serializer):
    """A field real people leave empty but naive bots fill in."""

    website_url = serializers.CharField(
        required=False, allow_blank=True, write_only=True
    )

    def validate_website_url(self, value):
        if value:
            raise serializers.ValidationError("Submission rejected.")
        return value


class ContactMessageSerializer(HoneypotMixin, serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id", "full_name", "email", "phone", "subject", "message",
            "website_url",
        ]

    def create(self, validated_data):
        validated_data.pop("website_url", None)
        return super().create(validated_data)


class VolunteerApplicationSerializer(HoneypotMixin, serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = [
            "id", "full_name", "email", "phone", "date_of_birth", "location",
            "occupation", "areas_of_interest", "skills", "availability",
            "motivation", "cv", "website_url",
        ]

    def create(self, validated_data):
        validated_data.pop("website_url", None)
        return super().create(validated_data)


class PartnerEnquirySerializer(HoneypotMixin, serializers.ModelSerializer):
    class Meta:
        model = PartnerEnquiry
        fields = [
            "id", "organisation_name", "contact_person", "email", "phone",
            "website", "country", "partnership_type", "message", "website_url",
        ]

    def create(self, validated_data):
        validated_data.pop("website_url", None)
        return super().create(validated_data)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email", "full_name", "source"]

    def create(self, validated_data):
        """Re-subscribing an existing address must not raise a 400."""
        email = validated_data["email"].lower().strip()
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                "full_name": validated_data.get("full_name", ""),
                "source": validated_data.get("source", ""),
            },
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save(update_fields=["is_active", "unsubscribed_at"])
        return subscriber


class DonationMethodSerializer(serializers.ModelSerializer):
    channel_label = serializers.CharField(
        source="get_channel_display", read_only=True
    )

    class Meta:
        model = DonationMethod
        fields = [
            "id", "channel", "channel_label", "label", "account_name",
            "account_number", "bank_name", "branch", "swift_code",
            "currency", "instructions", "icon",
        ]


class DonationPledgeSerializer(HoneypotMixin, serializers.ModelSerializer):
    class Meta:
        model = DonationPledge
        fields = [
            "id", "full_name", "email", "phone", "organisation", "amount",
            "currency", "method", "designation", "message", "is_anonymous",
            "website_url",
        ]

    def create(self, validated_data):
        validated_data.pop("website_url", None)
        return super().create(validated_data)
