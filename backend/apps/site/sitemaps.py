"""Sitemap for search engines, built from what is actually published."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.gallery.models import Album
from apps.news.models import Event, Post
from apps.programmes.models import FocusArea, Programme


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return [
            "site:home", "site:about", "site:team", "site:focus_areas",
            "site:programmes", "site:resources", "site:news", "site:events",
            "site:gallery", "site:videos", "site:get_involved",
            "site:volunteer", "site:partner", "site:donate", "site:contact",
            "site:privacy",
        ]

    def location(self, item):
        return reverse(item)


class _ModelSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"
    priority = 0.7

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None)


class ProgrammeSitemap(_ModelSitemap):
    priority = 0.9

    def items(self):
        return Programme.objects.published()


class FocusAreaSitemap(_ModelSitemap):
    def items(self):
        return FocusArea.objects.published()


class PostSitemap(_ModelSitemap):
    changefreq = "weekly"

    def items(self):
        return Post.objects.published()


class EventSitemap(_ModelSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Event.objects.published()


class AlbumSitemap(_ModelSitemap):
    priority = 0.5

    def items(self):
        return Album.objects.published()


SITEMAPS = {
    "static": StaticSitemap,
    "programmes": ProgrammeSitemap,
    "focus-areas": FocusAreaSitemap,
    "posts": PostSitemap,
    "events": EventSitemap,
    "albums": AlbumSitemap,
}
