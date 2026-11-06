"""URL configuration for the Simply Green Organization website."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from apps.core.views import health_check
from apps.site.sitemaps import SITEMAPS

admin.site.site_header = "Simply Green Organization"
admin.site.site_title = "Simply Green admin"
admin.site.index_title = "Content management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("config.api_urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("healthz/", health_check, name="health-check"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
        name="robots",
    ),
    # The public site last, so its catch-all slugs cannot shadow the above.
    path("", include("apps.site.urls")),
]

handler404 = "apps.site.views.handler404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif not settings.USE_SUPABASE_STORAGE:
    # Uploads live on local disk because the Supabase Storage credentials are
    # not configured, so Django has to serve the /media/ URLs it hands out.
    # With the S3 keys set, media comes from Supabase's CDN and these routes
    # are not added at all.
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}
        ),
    ]
