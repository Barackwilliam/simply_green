"""Public forms.

Every form carries a honeypot: a field hidden from sight, from screen readers
and from tabbing, which only an automated filler completes. A non-empty value
is rejected without telling the sender why, so a bot learns nothing.
"""

from django import forms

from apps.engage.models import (
    ContactMessage,
    DonationPledge,
    NewsletterSubscriber,
    PartnerEnquiry,
    VolunteerApplication,
)
from apps.news.models import EventRegistration


class HoneypotMixin(forms.Form):
    website_url = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website_url(self):
        if self.cleaned_data.get("website_url"):
            raise forms.ValidationError("Submission rejected.")
        return ""


class ContactForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone", "subject", "message"]
        labels = {"full_name": "Your name", "email": "Email address"}
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6}),
            "phone": forms.TextInput(attrs={"placeholder": "+255 …"}),
        }


class VolunteerForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = [
            "full_name", "email", "phone", "location", "occupation",
            "availability", "areas_of_interest", "skills", "motivation", "cv",
        ]
        labels = {
            "full_name": "Full name",
            "location": "Where you are based",
            "occupation": "Occupation or studies",
            "areas_of_interest": "What you would like to work on",
            "skills": "Skills you bring",
            "motivation": "Why you want to volunteer",
            "cv": "CV (PDF or Word)",
        }
        widgets = {
            "areas_of_interest": forms.Textarea(attrs={"rows": 3}),
            "skills": forms.Textarea(attrs={"rows": 3}),
            "motivation": forms.Textarea(attrs={"rows": 4}),
            "availability": forms.TextInput(
                attrs={"placeholder": "e.g. weekends, two days a week"}
            ),
        }


class PartnerForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = PartnerEnquiry
        fields = [
            "organisation_name", "contact_person", "email", "phone",
            "website", "country", "partnership_type", "message",
        ]
        labels = {"organisation_name": "Organisation", "message": "Tell us what you have in mind"}
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}


class NewsletterForm(HoneypotMixin, forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(required=False, max_length=180)


class DonationPledgeForm(HoneypotMixin, forms.ModelForm):
    """Records intent to give. Never asks for a card number, PIN or password."""

    class Meta:
        model = DonationPledge
        fields = [
            "full_name", "email", "phone", "organisation",
            "amount", "currency", "method", "designation",
            "message", "is_anonymous",
        ]
        labels = {
            "full_name": "Your name",
            "amount": "Amount (leave blank if you prefer not to say)",
            "method": "How you plan to give",
            "designation": "Programme you want to support",
            "is_anonymous": "Keep my gift anonymous in any public acknowledgement",
        }
        widgets = {"message": forms.Textarea(attrs={"rows": 3})}


class EventRegistrationForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ["full_name", "email", "phone", "organisation", "notes"]
        labels = {"notes": "Anything we should know"}
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
