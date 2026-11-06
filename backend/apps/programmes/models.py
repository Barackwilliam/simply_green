"""Focus areas and the programmes delivered under them."""

from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from apps.core.models import PublishableModel, SEOModel


class FocusArea(PublishableModel, SEOModel):
    """Thematic pillars: conservation, climate action, waste, and so on."""

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = models.TextField(
        help_text="One paragraph shown on the home page and focus-area grid."
    )
    body = CKEditor5Field(
        blank=True, config_name="extends", help_text="Full description."
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide icon name, e.g. 'leaf', 'cloud-sun', 'recycle'.",
    )
    image = models.ImageField(upload_to="focus-areas/", blank=True, null=True)
    accent_colour = models.CharField(
        max_length=7,
        blank=True,
        help_text="Optional hex colour for this area's cards, e.g. #11A2D7.",
    )

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Focus area"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)


class Programme(PublishableModel, SEOModel):
    """A programme or project, current or completed."""

    class Status(models.TextChoices):
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        PLANNED = "planned", "Planned"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="The longer descriptive line, e.g. 'Best Practice Training, "
        "Environmental Leadership and Sustainable Waste Management Programme'.",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ONGOING, db_index=True
    )
    focus_areas = models.ManyToManyField(
        FocusArea, related_name="programmes", blank=True
    )

    summary = models.TextField(help_text="Shown on programme cards. 2-3 sentences.")
    body = CKEditor5Field(config_name="extends", blank=True)

    featured_image = models.ImageField(
        upload_to="programmes/", blank=True, null=True
    )

    # --- Where and who ------------------------------------------------
    location = models.CharField(
        max_length=250,
        blank=True,
        help_text="e.g. 'Tandika Market, Temeke, Dar es Salaam'.",
    )
    region = models.CharField(max_length=120, blank=True)
    district = models.CharField(max_length=120, blank=True)
    beneficiaries = models.CharField(
        max_length=300,
        blank=True,
        help_text="e.g. 'Market traders, women and youth'.",
    )
    beneficiary_count = models.PositiveIntegerField(
        blank=True, null=True, help_text="Number of people reached, if known."
    )

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    partners = models.ManyToManyField(
        "core.Partner", related_name="programmes", blank=True
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured programmes appear on the home page."
    )

    class Meta:
        ordering = ["display_order", "-start_date", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:280]
        super().save(*args, **kwargs)


class ProgrammeOutcome(models.Model):
    """A measurable result attached to a programme."""

    programme = models.ForeignKey(
        Programme, related_name="outcomes", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=200, help_text="e.g. 'Traders trained'")
    value = models.CharField(max_length=40, help_text="e.g. '120'")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Programme outcome"

    def __str__(self):
        return f"{self.value} — {self.label}"


class ProgrammeImage(models.Model):
    """Extra photographs shown in a programme's gallery strip."""

    programme = models.ForeignKey(
        Programme, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="programmes/gallery/")
    caption = models.CharField(max_length=250, blank=True)
    alt_text = models.CharField(
        max_length=250,
        blank=True,
        help_text="Describes the photo for screen readers and search engines.",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Programme image"

    def __str__(self):
        return self.caption or f"Image for {self.programme}"
