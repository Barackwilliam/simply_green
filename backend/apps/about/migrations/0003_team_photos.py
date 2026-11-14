"""Swap the admin uploads for Anitha's and Kelvin's photographs for crops.

Both were uploaded in the admin as they came: Anitha's a 600x600 passport
shot with her head in the middle of a wide white ground, Kelvin's a
seated photograph with him small in the frame, so in the team page's
circle their faces came out small. Clearing the field here, once, lets
seed_team (which runs after migrate in the build) attach the versions in
assets/source/team/web, cropped to the same 4:5 frame as everyone
else's. A photograph uploaded in the admin after this runs is left alone.
"""

from django.db import migrations

PEOPLE = [
    ("Anitha Lwankomezi", "anitha-lwankomezi"),
    ("Kelvin Deodatus Mkatte", "kelvin-deodatus-mkatte"),
]


def forwards(apps, schema_editor):
    TeamMember = apps.get_model("about", "TeamMember")
    for name, stem in PEOPLE:
        member = TeamMember.objects.filter(full_name=name).first()
        if member and member.photo and stem not in member.photo.name:
            member.photo = ""
            member.save(update_fields=["photo"])


class Migration(migrations.Migration):
    dependencies = [("about", "0002_team_corrections")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
