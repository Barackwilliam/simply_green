from django.conf import settings
from django.core.mail import send_mail
from rest_framework import mixins, viewsets
from rest_framework.throttling import AnonRateThrottle

from apps.engage.models import (
    ContactMessage,
    DonationMethod,
    DonationPledge,
    NewsletterSubscriber,
    PartnerEnquiry,
    VolunteerApplication,
)

from .serializers import (
    ContactMessageSerializer,
    DonationMethodSerializer,
    DonationPledgeSerializer,
    NewsletterSubscriberSerializer,
    PartnerEnquirySerializer,
    VolunteerApplicationSerializer,
)


class SubmissionThrottle(AnonRateThrottle):
    """Tighter limit for endpoints that write to the database."""

    rate = "10/hour"


class _SubmitViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Write-only base: the public submits, only staff can read."""

    throttle_classes = [SubmissionThrottle]
    notify_subject = ""

    def perform_create(self, serializer):
        instance = serializer.save()
        self._notify(instance)

    def _notify(self, instance):
        recipients = getattr(settings, "NOTIFICATION_RECIPIENTS", [])
        if not recipients or not self.notify_subject:
            return
        try:
            send_mail(
                subject=f"[Simply Green] {self.notify_subject}",
                message=str(instance),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=True,
            )
        except Exception:
            pass


class ContactMessageViewSet(_SubmitViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    notify_subject = "New contact message"

    def perform_create(self, serializer):
        ip = self.request.META.get("REMOTE_ADDR")
        instance = serializer.save(source_ip=ip)
        self._notify(instance)


class VolunteerApplicationViewSet(_SubmitViewSet):
    queryset = VolunteerApplication.objects.all()
    serializer_class = VolunteerApplicationSerializer
    notify_subject = "New volunteer application"


class PartnerEnquiryViewSet(_SubmitViewSet):
    queryset = PartnerEnquiry.objects.all()
    serializer_class = PartnerEnquirySerializer
    notify_subject = "New partner enquiry"


class DonationPledgeViewSet(_SubmitViewSet):
    queryset = DonationPledge.objects.all()
    serializer_class = DonationPledgeSerializer
    notify_subject = "New donation pledge"


class NewsletterSubscriberViewSet(_SubmitViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    notify_subject = ""


class DonationMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """Bank and mobile money details shown on the donate page."""

    queryset = DonationMethod.objects.published()
    serializer_class = DonationMethodSerializer
    pagination_class = None
