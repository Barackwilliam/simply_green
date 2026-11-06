from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    list_display = (
        "title", "kind", "year", "published_date",
        "file_size_label", "download_count", "is_published",
    )
    list_editable = ("is_published",)
    list_filter = ("kind", "year", "is_featured", "is_published")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    readonly_fields = ("file_size_label", "download_count")
    fieldsets = (
        (None, {"fields": ("title", "slug", "kind", "programme")}),
        ("Document", {
            "fields": (
                "file", "external_url", "cover_image",
                "file_size_label", "page_count",
            ),
        }),
        ("Details", {"fields": ("summary", "published_date", "year")}),
        ("Search engines", {
            "fields": ("meta_title", "meta_description", "og_image", "noindex"),
            "classes": ("collapse",),
        }),
        ("Visibility", {
            "fields": ("is_featured", "is_published", "display_order",
                       "download_count"),
        }),
    )
