from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import (
    HeroSlide, ImageRendition, ImpactStat, Partner, SiteSettings, SocialLink,
)


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


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = (
        "preview", "headline", "eyebrow", "is_published", "display_order",
    )
    list_display_links = ("headline",)
    list_editable = ("is_published", "display_order")
    list_filter = ("is_published",)
    search_fields = ("headline", "subheadline")
    fieldsets = (
        ("Picture", {
            "fields": ("image", "image_alt"),
            "description": (
                "Landscape photographs work best. Large files are resized "
                "automatically, so upload the original."
            ),
        }),
        ("Words", {"fields": ("eyebrow", "headline", "subheadline")}),
        ("Buttons", {
            "fields": (
                "primary_label", "primary_url",
                "secondary_label", "secondary_url",
            ),
            "description": "Leave a label empty to hide that button.",
        }),
        ("Visibility", {"fields": ("is_published", "display_order")}),
    )

    @admin.display(description="")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:44px;width:78px;'
                'border-radius:4px;object-fit:cover;" />',
                obj.image.url,
            )
        return "—"


@admin.register(ImageRendition)
class ImageRenditionAdmin(ModelAdmin):
    """Where a photograph gets cropped.

    Most frames on the site are wider than they are tall, and a good number
    of the photographs come off a phone held upright. When those meet, more
    than half the picture is outside the frame, and whoever was standing at
    the edge is gone. This is where that is fixed: move the focus towards
    the part that matters and every place the photo appears follows.

    The rows themselves are made automatically on upload. Nothing here
    needs adding by hand.
    """

    list_display = ("preview", "source", "shape", "focus")
    list_display_links = ("preview", "source")
    search_fields = ("source",)
    readonly_fields = ("source", "width", "height", "variants", "preview_large")
    fields = ("preview_large", "source", "width", "height", "focal_x", "focal_y", "variants")

    def has_add_permission(self, request):
        return False

    @admin.display(description="")
    def preview(self, obj):
        url = self._url(obj)
        if not url:
            return "—"
        return format_html(
            '<img src="{}" style="width:76px;height:52px;object-fit:cover;'
            'object-position:{}% {}%;border-radius:6px">',
            url, obj.focal_x, obj.focal_y,
        )

    @admin.display(description="Shape")
    def shape(self, obj):
        if not obj.height:
            return "—"
        if obj.is_portrait:
            return format_html(
                '<span style="color:#b2660c;font-weight:700">Upright</span> '
                '<span style="color:#6d786f">{}&times;{} — wide frames will '
                'crop this; set the focus below</span>',
                obj.width, obj.height,
            )
        return format_html(
            '<span style="color:#6d786f">Landscape {}&times;{}</span>',
            obj.width, obj.height,
        )

    @admin.display(description="Focus")
    def focus(self, obj):
        return f"{obj.focal_x}% / {obj.focal_y}%"

    @admin.display(description="How it will be cropped")
    def preview_large(self, obj):
        url = self._url(obj)
        if not url:
            return "—"
        # The three shapes the site actually uses, side by side, so the
        # effect of moving the focus is visible without hunting for the page.
        frames = (("Hero band", "320px", "150px"),
                  ("Card", "220px", "138px"),
                  ("Portrait", "130px", "173px"))
        cells = "".join(
            format_html(
                '<figure style="margin:0 14px 0 0;display:inline-block;'
                'vertical-align:top">'
                '<img src="{}" style="width:{};height:{};object-fit:cover;'
                'object-position:{}% {}%;border-radius:8px;display:block">'
                '<figcaption style="font-size:11px;color:#6d786f;'
                'margin-top:5px">{}</figcaption></figure>',
                url, w, h, obj.focal_x, obj.focal_y, label,
            )
            for label, w, h in frames
        )
        return format_html("<div>{}</div>", cells)

    def _url(self, obj):
        from django.core.files.storage import default_storage

        path = obj.variants.get("420") or obj.variants.get("760") or obj.source
        try:
            return default_storage.url(path)
        except Exception:
            return ""
