"""Set the organisation's office address, postal address and phone number.

A data migration rather than a line in seed_content: seed_content leaves
site settings alone once they are filled in, so it would never reach the
live site, and a migration runs exactly once. Anything changed in the
admin afterwards stays changed.
"""

from django.db import migrations

ADDRESS = (
    "Auditax Building, Block 23\n"
    "Coca-Cola Road, Mikocheni B\n"
    "Dar es Salaam, Tanzania"
)
POSTAL = "P.O. Box 10107, Dar es Salaam"
PHONE = "+255 717 360 054"


def set_contact(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    settings, _ = SiteSettings.objects.get_or_create(pk=1)
    settings.address = ADDRESS
    settings.postal_address = POSTAL
    settings.phone = PHONE
    settings.city = "Dar es Salaam"
    settings.save(update_fields=["address", "postal_address", "phone", "city"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_imagerendition_focal_x_and_more"),
    ]

    operations = [
        migrations.RunPython(set_contact, migrations.RunPython.noop),
    ]
