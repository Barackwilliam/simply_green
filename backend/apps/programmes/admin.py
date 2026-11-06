from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import FocusArea, Programme, ProgrammeImage, ProgrammeOutcome


@admin.register(FocusArea)
class FocusAreaAdmin(ModelAdmin):
    list_display = ("title", "icon", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "icon", "accent_colour", "image")}),
        ("Content", {"fields": ("summary", "body")}),
        ("Search engines", {
            "fields": ("meta_title", "meta_description", "og_image", "noindex"),
            "classes": ("collapse",),
        }),
        ("Visibility", {"fields": ("is_published", "display_order")}),
    )


class ProgrammeOutcomeInline(TabularInline):
    model = ProgrammeOutcome
    extra = 1
    fields = ("label", "value", "display_order")


class ProgrammeImageInline(TabularInline):
    model = ProgrammeImage
    extra = 1
    fields = ("image", "alt_text", "caption", "display_order")


@admin.register(Programme)
class ProgrammeAdmin(ModelAdmin):
    list_display = (
        "image_preview", "title", "status", "location",
        "is_featured", "is_published",
    )
    list_display_links = ("title",)
    list_editable = ("is_featured", "is_published")
    list_filter = ("status", "is_featured", "is_published", "focus_areas")
    search_fields = ("title", "subtitle", "summary", "location", "beneficiaries")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("focus_areas", "partners")
    date_hierarchy = "start_date"
    inlines = [ProgrammeOutcomeInline, ProgrammeImageInline]
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "subtitle", "status", "featured_image"),
        }),
        ("Content", {"fields": ("summary", "body")}),
        ("Classification", {"fields": ("focus_areas", "partners")}),
        ("Where and who", {
            "fields": (
                "location", "region", "district",
                "beneficiaries", "beneficiary_count",
            ),
        }),
        ("Dates", {"fields": ("start_date", "end_date")}),
        ("Search engines", {
            "fields": ("meta_title", "meta_description", "og_image", "noindex"),
            "classes": ("collapse",),
        }),
        ("Visibility", {"fields": ("is_featured", "is_published", "display_order")}),
    )

    @admin.display(description="")
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="height:36px;width:56px;'
                'border-radius:4px;object-fit:cover;" />',
                obj.featured_image.url,
            )
        return "—"
