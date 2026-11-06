"""Resource centre: reports, publications and downloadable documents."""

from django.db import models
from django.utils.text import slugify

from apps.core.models import PublishableModel, SEOModel


class Publication(PublishableModel, SEOModel):
    """Any downloadable document the organisation publishes."""

    class Kind(models.TextChoices):
        ANNUAL_REPORT = "annual_report", "Annual report"
        FINANCIAL_REPORT = "financial_report", "Financial report"
        IMPACT_REPORT = "impact_report", "Impact report"
        PROJECT_REPORT = "project_report", "Project report"
        STRATEGIC_PLAN = "strategic_plan", "Strategic plan"
        RESEARCH = "research", "Research / Publication"
        POLICY_BRIEF = "policy_brief", "Policy brief"
        OTHER = "other", "Other document"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    kind = models.CharField(
        max_length=30, choices=Kind.choices, default=Kind.OTHER, db_index=True
    )
    summary = models.TextField(blank=True, help_text="What this document covers.")

    file = models.FileField(
        upload_to="publications/",
        blank=True,
        null=True,
        help_text="Upload the PDF. Leave blank if you are linking out instead.",
    )
    external_url = models.URLField(
        blank=True, help_text="Use when the document is hosted elsewhere."
    )
    cover_image = models.ImageField(
        upload_to="publications/covers/", blank=True, null=True
    )

    published_date = models.DateField(
        blank=True, null=True, db_index=True, help_text="Date of publication."
    )
    year = models.PositiveIntegerField(
        blank=True, null=True, db_index=True, help_text="Reporting year, if relevant."
    )
    page_count = models.PositiveIntegerField(blank=True, null=True)
    file_size_label = models.CharField(
        max_length=20,
        blank=True,
        help_text="Filled in automatically on save when a file is uploaded.",
    )

    programme = models.ForeignKey(
        "programmes.Programme",
        related_name="publications",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ["-published_date", "display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:280]
        if self.file:
            try:
                size = self.file.size
                for unit in ("B", "KB", "MB", "GB"):
                    if size < 1024 or unit == "GB":
                        self.file_size_label = (
                            f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
                        )
                        break
                    size /= 1024
            except (ValueError, OSError):
                pass
        super().save(*args, **kwargs)

    @property
    def download_url(self):
        if self.file:
            return self.file.url
        return self.external_url or ""
