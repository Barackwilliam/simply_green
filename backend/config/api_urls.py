"""Public JSON API consumed by the Next.js frontend."""

from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.api.urls")),
    path("about/", include("apps.about.api.urls")),
    path("programmes/", include("apps.programmes.api.urls")),
    path("resources/", include("apps.resources.api.urls")),
    path("news/", include("apps.news.api.urls")),
    path("gallery/", include("apps.gallery.api.urls")),
    path("engage/", include("apps.engage.api.urls")),
]
