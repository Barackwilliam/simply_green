"""Data for the Unfold admin landing page.

This used to compute four counts, a to-do list and a library tally, and
none of it was ever shown: Unfold's stock index template renders the app
list and nothing else, and there was no template overriding it. The
numbers were worked out on every visit to the dashboard and thrown away.

They are rendered now, in templates/admin/index.html, alongside two things
this particular client needs more than metrics: a list of what is waiting
for a reply, and a checklist of the parts of the site that are still empty
and therefore invisible to visitors.

Called only from UnfoldAdminSite.index, so none of these queries run on
any other admin page.
"""

from django.db.models import F
from django.urls import reverse
from django.utils import timezone


def _admin_url(label, view="changelist", **params):
    """Reverse an admin url, with an optional query string."""
    url = reverse(f"admin:{label}_{view}")
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    return url


def dashboard_callback(request, context):
    """Give editors an at-a-glance view of content, enquiries and gaps."""
    from apps.about.models import CoreValue, Objective, TeamMember
    from apps.core.models import (
        HeroSlide, ImpactStat, Partner, SiteSettings, SocialLink,
    )
    from apps.core.renditions import ImageRendition
    from apps.engage.models import (
        ContactMessage,
        DonationPledge,
        NewsletterSubscriber,
        PartnerEnquiry,
        VolunteerApplication,
    )
    from apps.gallery.models import Album, Photo
    from apps.news.models import Event, Post
    from apps.programmes.models import FocusArea, Programme
    from apps.resources.models import Publication

    now = timezone.now()
    site = SiteSettings.load()

    # --- the four numbers worth leading with -----------------------------
    kpi = [
        {
            "title": "Published programmes",
            "metric": Programme.objects.filter(is_published=True).count(),
            "icon": "eco",
            "url": _admin_url("programmes_programme"),
        },
        {
            "title": "Published articles",
            "metric": Post.objects.filter(
                is_published=True, published_at__lte=now
            ).count(),
            "icon": "article",
            "url": _admin_url("news_post"),
        },
        {
            "title": "Upcoming events",
            "metric": Event.objects.filter(
                is_published=True, start_datetime__gte=now
            ).count(),
            "icon": "event",
            "url": _admin_url("news_event"),
        },
        {
            "title": "Newsletter subscribers",
            "metric": NewsletterSubscriber.objects.filter(is_active=True).count(),
            "icon": "mail",
            "url": _admin_url("engage_newslettersubscriber"),
        },
    ]

    # --- people waiting for a reply --------------------------------------
    waiting = [
        {
            "label": "Unread contact messages",
            "count": ContactMessage.objects.filter(is_read=False).count(),
            "icon": "forum",
            "url": _admin_url("engage_contactmessage", is_read__exact=0),
        },
        {
            "label": "New volunteer applications",
            "count": VolunteerApplication.objects.filter(status="new").count(),
            "icon": "volunteer_activism",
            "url": _admin_url("engage_volunteerapplication", status__exact="new"),
        },
        {
            "label": "New partner enquiries",
            "count": PartnerEnquiry.objects.filter(status="new").count(),
            "icon": "handshake",
            "url": _admin_url("engage_partnerenquiry", status__exact="new"),
        },
        {
            "label": "Pledges awaiting confirmation",
            "count": DonationPledge.objects.filter(status="pledged").count(),
            "icon": "savings",
            "url": _admin_url("engage_donationpledge", status__exact="pledged"),
        },
    ]
    waiting_now = [row for row in waiting if row["count"]]

    # --- what is still empty, and what that costs ------------------------
    # A section with no rows behind it does not render at all, so the page
    # a visitor sees is missing it entirely. Worth saying plainly rather
    # than leaving someone to wonder why the site looks sparse.
    checks = [
        {
            "label": "Home page slides",
            "done": HeroSlide.objects.filter(is_published=True).exists(),
            "hint": "The photographs and headlines the site opens with.",
            "url": _admin_url("core_heroslide"),
        },
        {
            "label": "Contact details",
            "done": bool(site.email and site.phone),
            "hint": "Without these the contact page shows an empty panel.",
            "url": _admin_url("core_sitesettings"),
        },
        {
            "label": "Impact statistics",
            "done": ImpactStat.objects.filter(is_published=True).exists(),
            "hint": "The figures strip on the home page is hidden until "
                    "there is at least one.",
            "url": _admin_url("core_impactstat"),
        },
        {
            "label": "Team members",
            "done": TeamMember.objects.filter(is_published=True).exists(),
            "hint": "The team page shows a placeholder until people are added.",
            "url": _admin_url("about_teammember"),
        },
        {
            "label": "Partner logos",
            "done": Partner.objects.filter(is_published=True).exists(),
            "hint": "The partner strip on the home page needs real logos.",
            "url": _admin_url("core_partner"),
        },
        {
            "label": "Photo albums",
            "done": Album.objects.filter(is_published=True).exists(),
            "hint": "The gallery is empty until an album is published.",
            "url": _admin_url("gallery_album"),
        },
        {
            "label": "Social media links",
            "done": SocialLink.objects.filter(is_published=True).exists(),
            "hint": "These also tell search engines which accounts are yours.",
            "url": _admin_url("core_sociallink"),
        },
    ]
    outstanding = [c for c in checks if not c["done"]]

    # --- photographs a wide frame will crop badly -------------------------
    upright = ImageRendition.objects.filter(width__lt=F("height")).count()

    # --- quick ways in ----------------------------------------------------
    actions = [
        {"label": "Write an article", "icon": "edit_note",
         "url": _admin_url("news_post", "add")},
        {"label": "Add an event", "icon": "event_available",
         "url": _admin_url("news_event", "add")},
        {"label": "Add a home page slide", "icon": "wallpaper",
         "url": _admin_url("core_heroslide", "add")},
        {"label": "Add a programme", "icon": "eco",
         "url": _admin_url("programmes_programme", "add")},
        {"label": "Create a photo album", "icon": "photo_library",
         "url": _admin_url("gallery_album", "add")},
        {"label": "Edit site settings", "icon": "settings",
         "url": _admin_url("core_sitesettings")},
    ]

    library = [
        {"label": "Focus areas", "count": FocusArea.objects.count(),
         "url": _admin_url("programmes_focusarea")},
        {"label": "Core values", "count": CoreValue.objects.count(),
         "url": _admin_url("about_corevalue")},
        {"label": "Objectives", "count": Objective.objects.count(),
         "url": _admin_url("about_objective")},
        {"label": "Team members", "count": TeamMember.objects.count(),
         "url": _admin_url("about_teammember")},
        {"label": "Albums", "count": Album.objects.count(),
         "url": _admin_url("gallery_album")},
        {"label": "Photographs", "count": Photo.objects.count(),
         "url": _admin_url("gallery_photo")},
        {"label": "Publications", "count": Publication.objects.count(),
         "url": _admin_url("resources_publication")},
        {"label": "Partners", "count": Partner.objects.count(),
         "url": _admin_url("core_partner")},
    ]

    # --- the last few things touched --------------------------------------
    recent_posts = list(Post.objects.order_by("-updated_at")[:6])

    context.update(
        {
            "greeting_name": (
                request.user.get_short_name() or request.user.get_username()
            ),
            "kpi": kpi,
            "waiting": waiting,
            "waiting_now": waiting_now,
            "waiting_total": sum(row["count"] for row in waiting),
            "setup_checks": checks,
            "setup_done": len(checks) - len(outstanding),
            "setup_total": len(checks),
            "upright_images": upright,
            "upright_url": _admin_url("core_imagerendition"),
            "quick_actions": actions,
            "library": library,
            "recent_posts": recent_posts,
        }
    )
    return context
