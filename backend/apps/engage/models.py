"""Ways the public engages: volunteering, partnering, donating, enquiries."""

from django.db import models

from apps.core.models import PublishableModel, TimeStampedModel


class ContactMessage(TimeStampedModel):
    """A message sent through the contact form."""

    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False, db_index=True)
    is_archived = models.BooleanField(default=False)
    internal_notes = models.TextField(
        blank=True, help_text="Private — never shown to the sender."
    )

    # Light spam defence; filled by the API, not by the sender.
    source_ip = models.GenericIPAddressField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"

    def __str__(self):
        return f"{self.full_name} — {self.subject or 'No subject'}"


class VolunteerApplication(TimeStampedModel):
    """Someone offering to volunteer."""

    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWING = "reviewing", "Under review"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        WITHDRAWN = "withdrawn", "Withdrawn"

    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(
        max_length=200, blank=True, help_text="Where the applicant is based."
    )
    occupation = models.CharField(max_length=180, blank=True)

    areas_of_interest = models.TextField(
        blank=True,
        help_text="Which focus areas or programmes the applicant wants to join.",
    )
    skills = models.TextField(blank=True)
    availability = models.CharField(
        max_length=200, blank=True, help_text="e.g. 'Weekends', 'Two days a week'."
    )
    motivation = models.TextField(
        blank=True, help_text="Why they want to volunteer."
    )
    cv = models.FileField(upload_to="volunteers/cv/", blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, db_index=True
    )
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Volunteer application"

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"


class PartnerEnquiry(TimeStampedModel):
    """An organisation proposing a partnership or offering funding."""

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_DISCUSSION = "in_discussion", "In discussion"
        AGREED = "agreed", "Agreed"
        DECLINED = "declined", "Declined"

    organisation_name = models.CharField(max_length=220)
    contact_person = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=120, blank=True)

    partnership_type = models.CharField(
        max_length=200,
        blank=True,
        help_text="e.g. 'Funding', 'Technical support', 'Joint implementation'.",
    )
    message = models.TextField()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, db_index=True
    )
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Partner enquiry"
        verbose_name_plural = "Partner enquiries"

    def __str__(self):
        return f"{self.organisation_name} — {self.contact_person}"


class NewsletterSubscriber(TimeStampedModel):
    """Someone subscribed to email updates."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(
        max_length=100,
        blank=True,
        help_text="Where they signed up, e.g. 'footer', 'blog'.",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter subscriber"

    def __str__(self):
        return self.email


class DonationMethod(PublishableModel):
    """A bank account or mobile money channel shown on the donate page.

    These details are published on the website, so they hold no secrets —
    but they must be verified with the organisation's leadership directly
    before going live, not taken from an email alone.
    """

    class Channel(models.TextChoices):
        BANK = "bank", "Bank transfer"
        MPESA = "mpesa", "M-Pesa"
        TIGOPESA = "tigopesa", "Mixx by Yas (Tigo Pesa)"
        AIRTEL = "airtelmoney", "Airtel Money"
        HALOPESA = "halopesa", "HaloPesa"
        AZAMPESA = "azampesa", "Azam Pesa"
        OTHER = "other", "Other"

    channel = models.CharField(
        max_length=20, choices=Channel.choices, default=Channel.BANK
    )
    label = models.CharField(
        max_length=150, help_text="e.g. 'CRDB Bank — Tanzanian Shilling account'."
    )
    account_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(
        max_length=120,
        blank=True,
        help_text="Account number, Lipa Namba, or till number.",
    )
    bank_name = models.CharField(max_length=180, blank=True)
    branch = models.CharField(max_length=180, blank=True)
    swift_code = models.CharField(max_length=40, blank=True)
    currency = models.CharField(max_length=10, blank=True, default="TZS")
    instructions = models.TextField(
        blank=True, help_text="Any extra steps the donor should follow."
    )
    icon = models.ImageField(
        upload_to="donations/", blank=True, null=True, help_text="Bank or network logo."
    )

    class Meta:
        ordering = ["display_order", "label"]
        verbose_name = "Donation method"

    def __str__(self):
        return self.label


class DonationPledge(TimeStampedModel):
    """A donor telling the organisation they intend to give.

    This records intent only. No card or mobile-money credentials are
    collected or stored here.
    """

    class Status(models.TextChoices):
        PLEDGED = "pledged", "Pledged"
        CONFIRMED = "confirmed", "Received"
        CANCELLED = "cancelled", "Cancelled"

    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    organisation = models.CharField(max_length=200, blank=True)

    amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField(max_length=10, default="TZS")
    method = models.ForeignKey(
        DonationMethod,
        related_name="pledges",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    designation = models.CharField(
        max_length=200,
        blank=True,
        help_text="Which programme the donor wants to support, if any.",
    )
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLEDGED, db_index=True
    )
    reference = models.CharField(
        max_length=120, blank=True, help_text="Transaction reference, once received."
    )
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Donation pledge"

    def __str__(self):
        who = "Anonymous" if self.is_anonymous else self.full_name
        return f"{who} — {self.amount or '—'} {self.currency}"
