"""Andrew Malando William's description, as the client sent it."""

from django.db import migrations

BIO = (
    "Andrew spearheads community engagement, grassroots mobilization, and "
    "environmental awareness campaigns at Simply Green Organization, "
    "empowering local communities and youth to lead sustainable conservation "
    "efforts."
)


def forwards(apps, schema_editor):
    TeamMember = apps.get_model("about", "TeamMember")
    member = TeamMember.objects.filter(full_name="Andrew Malando William").first()
    if member and not member.bio:
        member.bio = f"<p>{BIO}</p>"
        member.short_bio = BIO
        member.save(update_fields=["bio", "short_bio"])


class Migration(migrations.Migration):
    dependencies = [("about", "0004_anitha_photo_wider")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
