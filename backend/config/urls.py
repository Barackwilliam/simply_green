"""URL configuration for the Simply Green Organization backend."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

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
