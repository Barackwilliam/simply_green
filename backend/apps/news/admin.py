from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Category, Event, EventRegistration, Post


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "colour", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = (
        "image_preview", "title", "kind", "category",
        "published_at", "is_featured", "is_published",
    )
    list_display_links = ("title",)
    list_editable = ("is_featured", "is_published")
    list_filter = ("kind", "category", "is_featured", "is_published", "published_at")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    autocomplete_fields = ("programme",)
    readonly_fields = ("reading_minutes", "view_count")
    fieldsets = (
        (None, {"fields": ("kind", "title", "slug", "category", "tags")}),
        ("Content", {"fields": ("excerpt", "body")}),
        ("Featured image", {
            "fields": (
                "featured_image", "featured_image_alt", "featured_image_credit",
            ),
        }),
        ("Attribution", {"fields": ("author", "author_name", "programme")}),
        ("Podcast", {
            "fields": ("audio_url", "audio_file"),
            "classes": ("collapse",),
            "description": "Only needed when the post type is Podcast.",
        }),
        ("Search engines", {
            "fields": ("meta_title", "meta_description", "og_image", "noindex"),
            "classes": ("collapse",),
        }),
        ("Publishing", {
            "fields": (
                "published_at", "is_featured", "is_published",
                "display_order", "reading_minutes", "view_count",
            ),
        }),
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


class EventRegistrationInline(TabularInline):
    model = EventRegistration
    extra = 0
    can_delete = False
    fields = (
        "full_name", "email", "phone", "organisation",
        "is_confirmed", "is_cancelled", "created_at",
    )
    readonly_fields = ("full_name", "email", "phone", "organisation", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = (
        "title", "start_datetime", "status", "venue",
        "registration_count", "is_published",
    )
    list_editable = ("is_published",)
    list_filter = ("status", "is_online", "is_featured", "is_published")
    search_fields = ("title", "summary", "venue")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"
    inlines = [EventRegistrationInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "status", "featured_image")}),
        ("Content", {"fields": ("summary", "body")}),
        ("When", {"fields": ("start_datetime", "end_datetime")}),
        ("Where", {
            "fields": (
                "venue", "address", "map_embed_url", "is_online", "online_url",
            ),
        }),
        ("Registration", {
            "fields": (
                "registration_enabled", "registration_deadline", "capacity",
            ),
        }),
        ("Links", {"fields": ("programme",)}),
        ("Search engines", {
            "fields": ("meta_title", "meta_description", "og_image", "noindex"),
            "classes": ("collapse",),
        }),
        ("Visibility", {"fields": ("is_featured", "is_published", "display_order")}),
    )

    @admin.display(description="Registered")
    def registration_count(self, obj):
        return obj.registrations.filter(is_cancelled=False).count()


@admin.register(EventRegistration)
class EventRegistrationAdmin(ModelAdmin):
    list_display = (
        "full_name", "email", "event", "is_confirmed",
        "is_cancelled", "created_at",
    )
    list_editable = ("is_confirmed", "is_cancelled")
    list_filter = ("event", "is_confirmed", "is_cancelled")
    search_fields = ("full_name", "email", "organisation")
    readonly_fields = ("created_at", "updated_at")
