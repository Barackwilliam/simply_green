"""Data for the Unfold admin landing page."""

from django.utils import timezone


def dashboard_callback(request, context):
    """Give editors an at-a-glance view of content and incoming enquiries."""
    from apps.about.models import TeamMember
    from apps.engage.models import (
        ContactMessage,
        DonationPledge,
        NewsletterSubscriber,
        PartnerEnquiry,
        VolunteerApplication,
    )
    from apps.gallery.models import Album, Photo
    from apps.news.models import Event, Post
    from apps.programmes.models import Programme
    from apps.resources.models import Publication

    now = timezone.now()

    context.update(
        {
            "kpi": [
                {
                    "title": "Published programmes",
                    "metric": Programme.objects.filter(is_published=True).count(),
                },
                {
                    "title": "Published posts",
                    "metric": Post.objects.filter(
                        is_published=True, published_at__lte=now
                    ).count(),
                },
                {
                    "title": "Upcoming events",
                    "metric": Event.objects.filter(
                        is_published=True, start_datetime__gte=now
                    ).count(),
                },
                {
                    "title": "Publications",
                    "metric": Publication.objects.filter(is_published=True).count(),
                },
            ],
            "needs_attention": [
                {
                    "label": "Unread contact messages",
                    "count": ContactMessage.objects.filter(is_read=False).count(),
                    "url": "/admin/engage/contactmessage/?is_read__exact=0",
                },
                {
                    "label": "New volunteer applications",
                    "count": VolunteerApplication.objects.filter(status="new").count(),
                    "url": "/admin/engage/volunteerapplication/?status__exact=new",
                },
                {
                    "label": "New partner enquiries",
                    "count": PartnerEnquiry.objects.filter(status="new").count(),
                    "url": "/admin/engage/partnerenquiry/?status__exact=new",
                },
                {
                    "label": "Pledges awaiting confirmation",
                    "count": DonationPledge.objects.filter(status="pledged").count(),
                    "url": "/admin/engage/donationpledge/?status__exact=pledged",
                },
            ],
            "library": [
                {"label": "Team members", "count": TeamMember.objects.count()},
                {"label": "Albums", "count": Album.objects.count()},
                {"label": "Photos", "count": Photo.objects.count()},
                {
                    "label": "Newsletter subscribers",
                    "count": NewsletterSubscriber.objects.filter(
                        is_active=True
                    ).count(),
                },
            ],
        }
    )
    return context
