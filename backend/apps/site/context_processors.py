"""Values every template needs: site settings, navigation, social links."""

from django.utils import timezone

from apps.core.models import SiteSettings, SocialLink

from .navigation import build_nav


def site_context(request):
    settings_obj = SiteSettings.load()
    return {
        "site": settings_obj,
        "social_links": SocialLink.objects.published(),
        "nav": build_nav(request.path),
        "current_year": timezone.now().year,
        "canonical_url": request.build_absolute_uri(request.path),
        "site_base_url": f"{request.scheme}://{request.get_host()}",
    }
