"""The organisation's email, second phone number and social profiles.

A data migration, like 0005, so it reaches the live database once and an
edit in the admin afterwards stays. X is left out: the account does not
exist yet. Add it in the admin under Social links when it does.
"""

from django.db import migrations

EMAIL = "simplygreen@gmail.com"
SECOND_PHONE = "+255 791 742 901"

LINKS = [
    ("facebook", "https://www.facebook.com/share/19hSxEdBEf/", 0),
    ("instagram", "https://www.instagram.com/simplygreentz_org/", 1),
    ("linkedin", "https://www.linkedin.com/company/simply-green-organization/", 2),
]


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SocialLink = apps.get_model("core", "SocialLink")

    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    settings.email = EMAIL
    settings.secondary_phone = SECOND_PHONE
    settings.save(update_fields=["email", "secondary_phone"])

    for platform, url, order in LINKS:
        SocialLink.objects.update_or_create(
            platform=platform,
            defaults={"url": url, "display_order": order, "is_published": True},
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0005_contact_details")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
