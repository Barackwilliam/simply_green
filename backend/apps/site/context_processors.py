"""Values every template needs: site settings, navigation, social links."""

from urllib.parse import urlsplit

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from apps.core.models import ImpactStat, SiteSettings, SocialLink

from .navigation import build_nav

# Written by seed_sample_content on every row it creates.
SAMPLE_MARK = "[sample]"


def _media_origin():
    """The origin photographs are served from, when it is not this one.

    In production that is Supabase, and the hero image is the largest thing
    on the page. Without this the browser cannot start fetching it until it
    has done a DNS lookup and a TLS handshake with a host it has never
    spoken to — from Tanzania to Supabase that is most of a second before a
    single byte of the photograph moves.
    """
    parts = urlsplit(settings.MEDIA_URL or "")
    if not parts.scheme or not parts.netloc:
        return ""
    return f"{parts.scheme}://{parts.netloc}"


MEDIA_ORIGIN = _media_origin()


def _showing_sample_content():
    """True while the placeholder content is loaded.

    The footer says so, so that nobody reading the site takes invented
    figures and made-up names for the organisation's own record. Cached,
    because this runs on every page and the answer changes about twice in
    the life of the project.
    """
    flag = cache.get("sample-content")
    if flag is None:
        flag = ImpactStat.objects.filter(description=SAMPLE_MARK).exists()
        cache.set("sample-content", flag, 300)
    return flag


def _share_image(request, settings_obj):
    """The picture that shows when a page is shared, as an absolute url.

    Facebook, WhatsApp, LinkedIn and X all refuse a relative one, and the
    organisation had not set a default, so every share was a bare link.
    Falls back to the site logo, then to a bundled image, so there is
    always something.
    """
    from django.templatetags.static import static

    candidate = ""
    if getattr(settings_obj, "default_og_image", None):
        candidate = settings_obj.default_og_image.url
    else:
        # Not the logo: a share card is 1200x630, and a 577x187 logo in
        # that slot is a letterboxed smear in every WhatsApp preview.
        candidate = static("img/share-card.jpg")
    if candidate.startswith(("http://", "https://")):
        return candidate
    return request.build_absolute_uri(candidate)


def site_context(request):
    settings_obj = SiteSettings.load()
    return {
        "site": settings_obj,
        "social_links": SocialLink.objects.published(),
        "nav": build_nav(request.path),
        "current_year": timezone.now().year,
        "canonical_url": request.build_absolute_uri(request.path),
        "site_base_url": f"{request.scheme}://{request.get_host()}",
        "showing_sample_content": _showing_sample_content(),
        "media_origin": MEDIA_ORIGIN,
        "share_image": _share_image(request, settings_obj),
    }
