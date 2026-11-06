"""Who we are: values, objectives, partnership case, and the team."""

from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from apps.core.models import PublishableModel


class CoreValue(PublishableModel):
    """The values that guide the organisation's work."""

    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Lucide icon name, e.g. 'leaf', 'users', 'shield-check'.",
    )

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Core value"

    def __str__(self):
        return self.title


class Objective(PublishableModel):
    """Formal organisational objectives."""

    text = models.TextField(help_text="One objective per record.")

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.text[:90] + ("…" if len(self.text) > 90 else "")


class PartnerReason(PublishableModel):
    """'Why partner with us' — the case made to funders."""

    title = models.CharField(max_length=180)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Reason to partner"
        verbose_name_plural = "Why partner with us"

    def __str__(self):
        return self.title


class TeamMember(PublishableModel):
    """Staff, board and volunteers shown on the team page."""

    class Group(models.TextChoices):
        LEADERSHIP = "leadership", "Leadership"
        BOARD = "board", "Board of Directors"
        STAFF = "staff", "Staff"
        VOLUNTEER = "volunteer", "Volunteer"
        ADVISOR = "advisor", "Advisor"

    full_name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    role = models.CharField(max_length=180, help_text="Job title or position.")
    group = models.CharField(
        max_length=20, choices=Group.choices, default=Group.STAFF, db_index=True
    )
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = CKEditor5Field(blank=True, config_name="default")
    short_bio = models.CharField(
        max_length=300, blank=True, help_text="One or two lines for the team grid."
    )

    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    x_handle = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["display_order", "full_name"]
        verbose_name = "Team member"

    def __str__(self):
        return f"{self.full_name} — {self.role}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)[:200]
        super().save(*args, **kwargs)
