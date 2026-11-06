"""Tell the Next.js frontend when content changes.

The site is statically prerendered, so an edit in the admin is invisible until
the matching cache tag is dropped. Every model that appears on the site
registers here; on save or delete we post its tags to the frontend.

Failures are logged and swallowed: a frontend that is briefly unreachable
must never stop an editor saving their work. The cache lifetime means the
change still appears on its own within the hour.
"""

import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 5


def purge(*tags: str) -> None:
    """Ask the frontend to drop these cache tags."""
    base_url = getattr(settings, "FRONTEND_URL", "")
    secret = getattr(settings, "REVALIDATE_SECRET", "")

    if not base_url or not secret:
        logger.debug("Revalidation not configured; skipping tags %s", tags)
        return

    payload = json.dumps({"tags": list(tags)}).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/revalidate",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-revalidate-secret": secret,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status >= 400:
                logger.warning(
                    "Revalidation returned %s for tags %s", response.status, tags
                )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.warning("Revalidation failed for tags %s: %s", tags, exc)


def register():
    """Connect every content model to its cache tags."""
    from apps.about.models import CoreValue, Objective, PartnerReason, TeamMember
    from apps.core.models import ImpactStat, Partner, SiteSettings, SocialLink
    from apps.engage.models import DonationMethod
    from apps.gallery.models import Album, Photo, Video
    from apps.news.models import Category, Event, Post
    from apps.programmes.models import (
        FocusArea,
        Programme,
        ProgrammeImage,
        ProgrammeOutcome,
    )
    from apps.resources.models import Publication

    # model -> (static tags, attribute holding a slug for a scoped tag)
    registry = [
        (SiteSettings, ("site-settings",), None),
        (SocialLink, ("site-settings",), None),
        (Partner, ("partners",), None),
        (ImpactStat, ("impact-stats",), None),
        (CoreValue, ("about",), None),
        (Objective, ("about",), None),
        (PartnerReason, ("about",), None),
        (TeamMember, ("team",), None),
        (FocusArea, ("focus-areas",), "focus-area"),
        (Programme, ("programmes",), "programme"),
        (ProgrammeOutcome, ("programmes",), None),
        (ProgrammeImage, ("programmes",), None),
        (Publication, ("publications",), None),
        (Category, ("posts",), None),
        (Post, ("posts",), "post"),
        (Event, ("events",), "event"),
        (Album, ("gallery",), "album"),
        (Photo, ("gallery",), None),
        (Video, ("gallery",), None),
        (DonationMethod, ("donation-methods",), None),
    ]

    for model, tags, slug_prefix in registry:
        _connect(model, tags, slug_prefix)


def _connect(model, tags, slug_prefix):
    label = f"{model._meta.app_label}.{model._meta.model_name}"

    def handler(sender, instance, **kwargs):
        all_tags = list(tags)
        if slug_prefix:
            slug = getattr(instance, "slug", "")
            if slug:
                all_tags.append(f"{slug_prefix}:{slug}")
        purge(*all_tags)

    post_save.connect(
        handler, sender=model, weak=False, dispatch_uid=f"revalidate-save-{label}"
    )
    post_delete.connect(
        handler, sender=model, weak=False, dispatch_uid=f"revalidate-delete-{label}"
    )
