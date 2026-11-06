from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Album, Photo, Video


class PhotoInline(TabularInline):
    model = Photo
    extra = 3
    fields = ("image", "alt_text", "caption", "credit", "display_order")


@admin.register(Album)
class AlbumAdmin(ModelAdmin):
    list_display = (
        "cover_preview", "title", "date", "location",
        "photo_count", "is_published",
    )
    list_display_links = ("title",)
    list_editable = ("is_published",)
    list_filter = ("is_featured", "is_published", "date")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
    inlines = [PhotoInline]

    @admin.display(description="")
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height:36px;width:56px;'
                'border-radius:4px;object-fit:cover;" />',
                obj.cover_image.url,
            )
        return "—"

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.photos.count()


@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ("preview", "album", "caption", "alt_text", "display_order")
    list_display_links = ("caption",)
    list_filter = ("album",)
    search_fields = ("caption", "alt_text", "credit")

    @admin.display(description="")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:36px;width:56px;'
                'border-radius:4px;object-fit:cover;" />',
                obj.image.url,
            )
        return "—"


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ("title", "source", "date", "is_featured", "is_published")
    list_editable = ("is_featured", "is_published")
    list_filter = ("source", "is_featured", "is_published")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
