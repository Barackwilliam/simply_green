"""URL configuration for the Simply Green Organization backend."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from apps.core.views import health_check

admin.site.site_header = "Simply Green Organization"
admin.site.site_title = "Simply Green admin"
admin.site.index_title = "Content management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("config.api_urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("healthz/", health_check, name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif not settings.USE_SUPABASE_STORAGE:
    # Fallback mode: uploads are on local disk because the Supabase Storage
    # credentials are not configured. Django still hands out /media/ URLs for
    # them, so it has to answer those URLs too — otherwise every uploaded
    # image 404s and the site renders with broken pictures.
    #
    # This is the degraded path, not the intended one. With the S3 keys set,
    # media is served from Supabase's CDN and these routes are not added.
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
