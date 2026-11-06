from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ContactMessageViewSet,
    DonationMethodViewSet,
    DonationPledgeViewSet,
    NewsletterSubscriberViewSet,
    PartnerEnquiryViewSet,
    VolunteerApplicationViewSet,
)

router = DefaultRouter()
router.register("contact", ContactMessageViewSet, basename="contact")
router.register("volunteer", VolunteerApplicationViewSet, basename="volunteer")
router.register("partner-enquiry", PartnerEnquiryViewSet, basename="partner-enquiry")
router.register("newsletter", NewsletterSubscriberViewSet, basename="newsletter")
router.register("donate", DonationPledgeViewSet, basename="donate")
router.register(
    "donation-methods", DonationMethodViewSet, basename="donation-method"
)

urlpatterns = [path("", include(router.urls))]
