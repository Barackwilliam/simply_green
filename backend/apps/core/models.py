"""Shared base models plus site-wide singletons."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class TimeStampedModel(models.Model):
    """Adds created/updated bookkeeping to any model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(TimeStampedModel):
    """Content that editors can draft before it goes live."""

    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Untick to hide this from the website without deleting it.",
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Lower numbers appear first.",
    )

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Per-page search engine and social sharing overrides."""

    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Overrides the browser/Google title. Aim for 50-60 characters.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="The grey text Google shows under the title. Aim for 150-160 characters.",
    )
    og_image = models.ImageField(
        upload_to="seo/",
        blank=True,
        null=True,
        help_text="Image shown when the page is shared on social media. 1200x630 works best.",
    )
    noindex = models.BooleanField(
        default=False,
        help_text="Tick to ask search engines not to list this page.",
    )

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """A model with exactly one row — used for site-wide settings."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("This record is required and cannot be deleted.")

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel, TimeStampedModel):
    """Everything that appears on every page: identity, contact, SEO defaults."""

    # --- Identity -----------------------------------------------------
    organisation_name = models.CharField(
        max_length=200, default="Simply Green Organization"
    )
    acronym = models.CharField(max_length=20, default="SGO")
    tagline = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short phrase shown under the logo, e.g. in the footer.",
    )
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    logo_light = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Version for dark backgrounds, if you have one.",
    )
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)

    registration_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. 00NGO/R5315",
    )
    registration_statement = models.TextField(
        blank=True,
        help_text="Full registration sentence shown in the footer and About page.",
    )

    # --- Mission ------------------------------------------------------
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    who_we_are = CKEditor5Field(blank=True, config_name="extends")

    # --- Contact ------------------------------------------------------
    email = models.EmailField(blank=True)
    secondary_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    secondary_phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, default="Dar es Salaam")
    country = models.CharField(max_length=100, default="Tanzania")

    map_embed_url = models.URLField(
        blank=True,
        max_length=1000,
        help_text="Google Maps embed URL for the office location.",
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # --- Default SEO --------------------------------------------------
    default_meta_title = models.CharField(max_length=70, blank=True)
    default_meta_description = models.CharField(max_length=160, blank=True)
    default_og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    google_analytics_id = models.CharField(
        max_length=50, blank=True, help_text="e.g. G-XXXXXXXXXX"
    )
    google_site_verification = models.CharField(max_length=200, blank=True)

    # --- Calls to action ----------------------------------------------
    donate_enabled = models.BooleanField(default=True)
    volunteer_enabled = models.BooleanField(default=True)
    newsletter_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.organisation_name


class SocialLink(PublishableModel):
    """Social profiles rendered in the header and footer."""

    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        LINKEDIN = "linkedin", "LinkedIn"
        X = "x", "X (Twitter)"
        YOUTUBE = "youtube", "YouTube"
        TIKTOK = "tiktok", "TikTok"
        WHATSAPP = "whatsapp", "WhatsApp"
        TELEGRAM = "telegram", "Telegram"

    platform = models.CharField(
        max_length=20, choices=Platform.choices, unique=True
    )
    url = models.URLField()

    class Meta:
        ordering = ["display_order", "platform"]

    def __str__(self):
        return self.get_platform_display()


class Partner(PublishableModel):
    """Partners, donors and collaborators shown as a logo wall."""

    class Kind(models.TextChoices):
        PARTNER = "partner", "Partner"
        DONOR = "donor", "Donor / Funder"
        GOVERNMENT = "government", "Government institution"
        PRIVATE = "private", "Private sector"
        NETWORK = "network", "Network / Coalition"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    kind = models.CharField(
        max_length=20, choices=Kind.choices, default=Kind.PARTNER, db_index=True
    )
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(
        default=False, help_text="Featured partners appear on the home page."
    )

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)


class ImpactStat(PublishableModel):
    """Headline numbers — trees planted, people reached, waste collected."""

    label = models.CharField(
        max_length=120, help_text="e.g. 'Tonnes of waste collected'"
    )
    value = models.CharField(
        max_length=30, help_text="e.g. '12,400' or '3.2'. Shown exactly as typed."
    )
    suffix = models.CharField(
        max_length=20, blank=True, help_text="e.g. '+', 'kg', 'ha'"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide icon name, e.g. 'recycle', 'users', 'trees'.",
    )
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Impact statistic"

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class HeroSlide(PublishableModel):
    """One frame of the slideshow at the top of the home page.

    Managed here rather than hard-coded so the organisation can change what
    the site leads with — a campaign, a new programme, a call to act — without
    anyone touching the templates.
    """

    image = models.ImageField(
        upload_to="hero/",
        help_text="Landscape works best. Anything large is resized on upload.",
    )
    image_alt = models.CharField(
        max_length=250,
        blank=True,
        help_text="Describes the photograph for screen readers and search engines.",
    )
    eyebrow = models.CharField(
        max_length=80,
        blank=True,
        help_text="Small line above the headline, e.g. 'Registered NGO · Tanzania'.",
    )
    headline = models.CharField(max_length=180)
    subheadline = models.TextField(
        blank=True, help_text="One or two sentences under the headline."
    )

    primary_label = models.CharField(max_length=60, blank=True)
    primary_url = models.CharField(
        max_length=300,
        blank=True,
        help_text="A path such as /programmes/ or a full https:// address.",
    )
    secondary_label = models.CharField(max_length=60, blank=True)
    secondary_url = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Home page slide"

    def __str__(self):
        return self.headline


# Lives in its own module because it is machinery rather than content, but
# it has to be imported here for Django to see it as a model of this app.
from apps.core.renditions import ImageRendition  # noqa: E402,F401
