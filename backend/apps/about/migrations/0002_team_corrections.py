"""Corrections the client sent for three team members.

Athuman Alfred Ndoke is the Data Coordinator, not the Policy Coordinator;
Julius Eston is the Policy Coordinator, and takes the policy description;
Joyce Singu has her own description now.

A data migration because seed_team adds each person only once and never
touches them again, so its list alone would not reach the live site.
Each record is looked up by name; one that has been renamed or deleted
in the admin is left alone.
"""

from django.db import migrations

POLICY = (
    "Coordinates environmental policy development, advocacy, and stakeholder "
    "engagement to promote sustainable environmental governance. Supports the "
    "organisation in analysing environmental policies, strengthening "
    "institutional partnerships, and advocating for effective policies on "
    "climate action, sustainable waste management, biodiversity conservation, "
    "and sustainable development. Works to ensure that environmental policies "
    "promote community participation and long-term environmental "
    "sustainability."
)
DATA = (
    "Athuman manages the collection, verification, and analysis of "
    "environmental and community impact data at Simply Green Organization, "
    "ensuring accurate reporting and evidence-based decision-making across all "
    "programs."
)
JOYCE = (
    "Joyce Singu is the Community Outreach Officer at Simply Green "
    "Organization (SGO). As a Community Outreach Officer, my responsibility is "
    "to build good relationships between the organization and the community. "
    "I communicate with community members, provide education and encourage "
    "them to participate in development activities and projects. I also "
    "identify community needs and challenges, collect feedback and help find "
    "possible solutions. I organize community meetings and awareness "
    "campaigns, work with community leaders and prepare reports on activities "
    "carried out. Generally, my role is to ensure that community members "
    "receive important information, services and opportunities that can "
    "improve their lives."
)

CHANGES = [
    ("Athuman Alfred Ndoke", "Data Coordinator", DATA),
    ("Julius Eston", "Policy Coordinator", POLICY),
    ("Joyce Singu", None, JOYCE),
]


def summary(text, limit=300):
    first = text.split(". ")[0].rstrip(".") + "."
    return first if len(first) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + "…"


def forwards(apps, schema_editor):
    TeamMember = apps.get_model("about", "TeamMember")
    for name, role, bio in CHANGES:
        member = TeamMember.objects.filter(full_name=name).first()
        if member is None:
            continue
        if role:
            member.role = role
        member.bio = f"<p>{bio}</p>"
        member.short_bio = summary(bio)
        member.save(update_fields=["role", "bio", "short_bio"])


class Migration(migrations.Migration):
    dependencies = [("about", "0001_initial")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
