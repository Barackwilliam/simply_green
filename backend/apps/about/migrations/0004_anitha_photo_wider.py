"""Replace Anitha's photograph from 0003 with a wider crop.

The crop 0003 brought in was too tight: her neck did not show in the
team page's circle. This clears that one, recognised by its file name,
so seed_team attaches the wider version (anitha-lwankomezi-v2) on the
same deploy. A photograph uploaded in the admin since then has another
name and is left alone.
"""

from django.db import migrations


def forwards(apps, schema_editor):
    TeamMember = apps.get_model("about", "TeamMember")
    member = TeamMember.objects.filter(full_name="Anitha Lwankomezi").first()
    if member is None or not member.photo:
        return
    name = member.photo.name
    if "anitha-lwankomezi" in name and "anitha-lwankomezi-v2" not in name:
        member.photo = ""
        member.save(update_fields=["photo"])


class Migration(migrations.Migration):
    dependencies = [("about", "0003_team_photos")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
