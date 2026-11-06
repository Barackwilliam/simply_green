from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import ImpactStat, Partner, SiteSettings, SocialLink


class SingletonAdminMixin:
    """Site settings is a single record: no adding, no deleting."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, ModelAdmin):
    fieldsets = (
        ("Identity", {
            "fields": (
                "organisation_name", "acronym", "tagline",
                "logo", "logo_light", "favicon",
                "registration_number", "registration_statement",
            ),
        }),
        ("Mission", {"fields": ("vision", "mission", "who_we_are")}),
        ("Contact details", {
            "fields": (
                "email", "secondary_email", "phone", "secondary_phone",
                "whatsapp", "address", "postal_address", "city", "country",
            ),
        }),
        ("Map", {
            "fields": ("map_embed_url", "latitude", "longitude"),
            "classes": ("collapse",),
        }),
        ("Search engine defaults", {
            "fields": (
                "default_meta_title", "default_meta_description",
                "default_og_image", "google_analytics_id",
                "google_site_verification",
            ),
        }),
        ("Features", {
            "fields": ("donate_enabled", "volunteer_enabled", "newsletter_enabled"),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        """Jump straight into the single record instead of showing a list."""
        from django.shortcuts import redirect
        from django.urls import reverse

        obj = SiteSettings.load()
        return redirect(
            reverse("admin:core_sitesettings_change", args=[obj.pk])
        )


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ("platform", "url", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    list_display = (
        "logo_preview", "name", "kind", "is_featured",
        "is_published", "display_order",
    )
    list_display_links = ("name",)
    list_editable = ("is_featured", "is_published", "display_order")
    list_filter = ("kind", "is_featured", "is_published")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:28px;width:auto;'
                'object-fit:contain;" />',
                obj.logo.url,
            )
        return "—"


@admin.register(ImpactStat)
class ImpactStatAdmin(ModelAdmin):
    list_display = ("label", "value", "suffix", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
