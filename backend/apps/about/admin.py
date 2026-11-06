from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import CoreValue, Objective, PartnerReason, TeamMember


@admin.register(CoreValue)
class CoreValueAdmin(ModelAdmin):
    list_display = ("title", "icon", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    search_fields = ("title", "description")


@admin.register(Objective)
class ObjectiveAdmin(ModelAdmin):
    list_display = ("__str__", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    search_fields = ("text",)


@admin.register(PartnerReason)
class PartnerReasonAdmin(ModelAdmin):
    list_display = ("title", "icon", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    search_fields = ("title", "description")


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = (
        "photo_preview", "full_name", "role", "group",
        "is_published", "display_order",
    )
    list_display_links = ("full_name",)
    list_editable = ("is_published", "display_order")
    list_filter = ("group", "is_published")
    search_fields = ("full_name", "role", "short_bio")
    prepopulated_fields = {"slug": ("full_name",)}
    fieldsets = (
        (None, {"fields": ("full_name", "slug", "role", "group", "photo")}),
        ("Biography", {"fields": ("short_bio", "bio")}),
        ("Contact", {"fields": ("email", "linkedin", "x_handle")}),
        ("Visibility", {"fields": ("is_published", "display_order")}),
    )

    @admin.display(description="")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:36px;width:36px;'
                'border-radius:50%;object-fit:cover;" />',
                obj.photo.url,
            )
        return "—"
