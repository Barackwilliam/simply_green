"""Photo albums and videos."""

from django.db import models
from django.utils.text import slugify

from apps.core.models import PublishableModel


class Album(PublishableModel):
    """A set of photographs, usually from one activity or event."""

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to="gallery/covers/", blank=True, null=True
    )
    date = models.DateField(blank=True, null=True, db_index=True)
    location = models.CharField(max_length=200, blank=True)

    programme = models.ForeignKey(
        "programmes.Programme",
        related_name="albums",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    event = models.ForeignKey(
        "news.Event",
        related_name="albums",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:250]
        super().save(*args, **kwargs)

    @property
    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    """A single image inside an album."""

    album = models.ForeignKey(
        Album, related_name="photos", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="gallery/photos/")
    caption = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(
        max_length=250,
        blank=True,
        help_text="Describes the photo for screen readers and search engines. "
        "Always fill this in.",
    )
    credit = models.CharField(max_length=150, blank=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class Video(PublishableModel):
    """An embedded or uploaded video."""

    class Source(models.TextChoices):
        YOUTUBE = "youtube", "YouTube"
        VIMEO = "vimeo", "Vimeo"
        UPLOAD = "upload", "Uploaded file"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField(blank=True)

    source = models.CharField(
        max_length=20, choices=Source.choices, default=Source.YOUTUBE
    )
    video_url = models.URLField(
        blank=True, help_text="Full YouTube or Vimeo URL."
    )
    video_file = models.FileField(
        upload_to="gallery/videos/", blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to="gallery/thumbnails/", blank=True, null=True
    )
    duration_label = models.CharField(
        max_length=20, blank=True, help_text="e.g. '4:32'"
    )
    date = models.DateField(blank=True, null=True, db_index=True)

    programme = models.ForeignKey(
        "programmes.Programme",
        related_name="videos",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:250]
        super().save(*args, **kwargs)
