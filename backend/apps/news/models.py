"""News, announcements, impact stories, podcasts and events."""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

from apps.core.models import PublishableModel, SEOModel, TimeStampedModel


class Category(PublishableModel):
    """Groups posts — e.g. 'Climate', 'Waste', 'Community'."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    colour = models.CharField(
        max_length=7, blank=True, help_text="Optional hex colour for the badge."
    )

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True, published_at__lte=timezone.now()
        )


class Post(PublishableModel, SEOModel):
    """A news article, announcement, impact story or podcast episode."""

    class Kind(models.TextChoices):
        NEWS = "news", "News"
        ANNOUNCEMENT = "announcement", "Announcement"
        IMPACT_STORY = "impact_story", "Impact story"
        PODCAST = "podcast", "Podcast"
        BLOG = "blog", "Blog post"

    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.NEWS, db_index=True
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    excerpt = models.TextField(
        max_length=400,
        blank=True,
        help_text="Short teaser shown on cards. If blank, the opening of the "
        "article is used.",
    )
    body = CKEditor5Field(config_name="extends", blank=True)

    featured_image = models.ImageField(upload_to="news/", blank=True, null=True)
    featured_image_alt = models.CharField(max_length=250, blank=True)
    featured_image_credit = models.CharField(max_length=150, blank=True)

    category = models.ForeignKey(
        Category,
        related_name="posts",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tags = TaggableManager(blank=True)
    programme = models.ForeignKey(
        "programmes.Programme",
        related_name="posts",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    author_name = models.CharField(max_length=150, blank=True)
    author = models.ForeignKey(
        "about.TeamMember",
        related_name="posts",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    published_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text="Set a future date to schedule this post.",
    )
    reading_minutes = models.PositiveSmallIntegerField(
        blank=True, null=True, editable=False
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured posts lead the news page."
    )
    view_count = models.PositiveIntegerField(default=0, editable=False)

    # Podcast-specific
    audio_url = models.URLField(
        blank=True, help_text="Podcast audio or episode link."
    )
    audio_file = models.FileField(
        upload_to="podcasts/", blank=True, null=True
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-id"]
        indexes = [
            models.Index(fields=["kind", "-published_at"]),
            models.Index(fields=["is_published", "-published_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:280]
        if self.body:
            words = len(self.body.split())
            self.reading_minutes = max(1, round(words / 200))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("site:post_detail", kwargs={"slug": self.slug})


class Event(PublishableModel, SEOModel):
    """An upcoming or past event, with optional online registration."""

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Happening now"
        PAST = "past", "Past"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    summary = models.TextField(blank=True)
    body = CKEditor5Field(config_name="extends", blank=True)
    featured_image = models.ImageField(upload_to="events/", blank=True, null=True)

    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPCOMING, db_index=True
    )

    venue = models.CharField(max_length=250, blank=True)
    address = models.TextField(blank=True)
    map_embed_url = models.URLField(max_length=1000, blank=True)
    is_online = models.BooleanField(default=False)
    online_url = models.URLField(blank=True)

    programme = models.ForeignKey(
        "programmes.Programme",
        related_name="events",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    registration_enabled = models.BooleanField(
        default=False, help_text="Tick to show a registration form on this event."
    )
    registration_deadline = models.DateTimeField(blank=True, null=True)
    capacity = models.PositiveIntegerField(
        blank=True, null=True, help_text="Leave blank for unlimited places."
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:280]
        super().save(*args, **kwargs)

    @property
    def is_full(self):
        if self.capacity is None:
            return False
        return self.registrations.filter(is_cancelled=False).count() >= self.capacity

    @property
    def registration_open(self):
        if not self.registration_enabled or self.status == self.Status.CANCELLED:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        return not self.is_full

    def get_absolute_url(self):
        return reverse("site:event_detail", kwargs={"slug": self.slug})


class EventRegistration(TimeStampedModel):
    """Someone signing up to attend an event."""

    event = models.ForeignKey(
        Event, related_name="registrations", on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    organisation = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["event", "email"]]
        verbose_name = "Event registration"

    def __str__(self):
        return f"{self.full_name} — {self.event}"
