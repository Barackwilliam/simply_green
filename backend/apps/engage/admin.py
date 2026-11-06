from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    ContactMessage,
    DonationMethod,
    DonationPledge,
    NewsletterSubscriber,
    PartnerEnquiry,
    VolunteerApplication,
)


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ("full_name", "email", "subject", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read", "is_archived", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = (
        "full_name", "email", "phone", "subject", "message",
        "source_ip", "created_at", "updated_at",
    )
    fieldsets = (
        ("Message", {
            "fields": ("full_name", "email", "phone", "subject", "message"),
        }),
        ("Handling", {"fields": ("is_read", "is_archived", "internal_notes")}),
        ("Metadata", {
            "fields": ("source_ip", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    actions = ["mark_read", "mark_unread"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected as unread")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(ModelAdmin):
    list_display = ("full_name", "email", "phone", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone", "skills", "motivation")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False


@admin.register(PartnerEnquiry)
class PartnerEnquiryAdmin(ModelAdmin):
    list_display = (
        "organisation_name", "contact_person", "email", "status", "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("organisation_name", "contact_person", "email", "message")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ("email", "full_name", "is_active", "source", "created_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "source", "created_at")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(DonationMethod)
class DonationMethodAdmin(ModelAdmin):
    list_display = (
        "label", "channel", "account_number", "currency",
        "is_published", "display_order",
    )
    list_editable = ("is_published", "display_order")
    list_filter = ("channel", "is_published")
    search_fields = ("label", "account_name", "account_number", "bank_name")
    fieldsets = (
        (None, {
            "fields": ("channel", "label", "icon"),
            "description": (
                "These details are published on the website. Verify every "
                "account number directly with the organisation's leadership "
                "before publishing — never from an email alone."
            ),
        }),
        ("Account", {
            "fields": (
                "account_name", "account_number", "bank_name",
                "branch", "swift_code", "currency",
            ),
        }),
        ("Guidance", {"fields": ("instructions",)}),
        ("Visibility", {"fields": ("is_published", "display_order")}),
    )


@admin.register(DonationPledge)
class DonationPledgeAdmin(ModelAdmin):
    list_display = (
        "__str__", "email", "designation", "status", "reference", "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status", "currency", "created_at")
    search_fields = ("full_name", "email", "organisation", "reference")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return False
