"""Load the organisation's team, as the client sent it, with photographs.

Each person is added once. After that the admin owns the record: a
changed role, description or order is never overwritten, and a removed
person is not brought back unless they are deleted outright. A photograph
is attached only when the record has none, or when the one it points at
is no longer in storage.

Photographs come from assets/source/team/web, cropped to the same 4:5
frame with the face in the upper third. The client's originals sit one
folder up.

Called from seed_content, which is in the build command, so it runs on
every deploy and costs nothing once the team is there.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.about.models import TeamMember

PHOTO_DIR = Path(settings.BASE_DIR).parent / "assets" / "source" / "team" / "web"

# (name, role, group, description, photograph file stem or "")
TEAM = [
    ('Adriano Gesa', 'Executive Director', 'leadership',
     'Adriano is a visionary leader dedicated to advancing environmental sustainability, climate resilience, and community empowerment. As Executive Director, he provides strategic leadership, fosters high-level partnerships, and guides organizational growth to deliver lasting ecological and social impact.',
     'adriano-gesa'),
    ('Amiri Bakari Mwera', 'Program Manager', 'leadership',
     'Amiri is dedicated to driving sustainable environmental change and community resilience. With 5 years of experience in the NGO sector, he excels at coordinating and supervising conservation initiatives, building multi-stakeholder partnerships, and delivering measurable ecological and social impact.',
     'amiri-bakari-mwera'),
    ('Teonestina Athanasi Kisogole', 'Finance and Administrative Officer', 'staff',
     "Teonestina Athanasi Kisogole is a Finance and Administrative Officer at Simply Green Organisation (SGO), with an academic background in Accountancy and practical experience in financial and administrative activities. She supports the organisation's financial management, maintains accurate financial records, monitors expenditures, and coordinates administrative operations. She is committed to ensuring financial transparency, accountability, and efficient administrative management in support of the organisation's goals and objectives.",
     'teonestina-athanasi-kisogole'),
    ('Julius Eston', 'Policy Coordinator', 'staff',
     'Coordinates environmental policy development, advocacy, and stakeholder engagement to promote sustainable environmental governance. Supports the organisation in analysing environmental policies, strengthening institutional partnerships, and advocating for effective policies on climate action, sustainable waste management, biodiversity conservation, and sustainable development. Works to ensure that environmental policies promote community participation and long-term environmental sustainability.',
     'julius-eston'),
    ('Kelvin Deodatus Mkatte', 'Media Coordinator', 'staff',
     "Kelvin Deodatus Mkatte is the Media Coordinator at Simply Green Organisation, bringing four years of expertise in digital media and visual storytelling. He leads the organization's social media management, graphic design, and professional video and photography production to amplify environmental conservation campaigns. Additionally, he spearheads the creation of the official company profile, ensuring the organization's mission and impact are powerfully communicated across all platforms.",
     'kelvin-deodatus-mkatte'),
    ('Athuman Alfred Ndoke', 'Data Coordinator', 'staff',
     'Athuman manages the collection, verification, and analysis of environmental and community impact data at Simply Green Organization, ensuring accurate reporting and evidence-based decision-making across all programs.',
     ''),
    ('Andrew Malando William', 'Community Outreach Officer', 'staff',
     'Andrew spearheads community engagement, grassroots mobilization, and environmental awareness campaigns at Simply Green Organization, empowering local communities and youth to lead sustainable conservation efforts.',
     'andrew-malando-william'),
    ('Joyce Singu', 'Community Outreach Officer', 'staff',
     'Joyce Singu is the Community Outreach Officer at Simply Green Organization (SGO). As a Community Outreach Officer, my responsibility is to build good relationships between the organization and the community. I communicate with community members, provide education and encourage them to participate in development activities and projects. I also identify community needs and challenges, collect feedback and help find possible solutions. I organize community meetings and awareness campaigns, work with community leaders and prepare reports on activities carried out. Generally, my role is to ensure that community members receive important information, services and opportunities that can improve their lives.',
     'joyce-singu'),
    ('Anitha Lwankomezi', 'Community Outreach Officer', 'staff',
     'Climate Change and Sustainable Development Professional.',
     'anitha-lwankomezi-v2'),
]


def _summary(text, limit=300):
    """short_bio holds 300 characters: the first sentence, or a clean cut."""
    first = text.split(". ")[0].rstrip(".") + "."
    if len(first) <= limit:
        return first
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


class Command(BaseCommand):
    help = "Add the organisation's team members and their photographs."

    def handle(self, *args, **options):
        added = photos = 0
        for order, (name, role, group, bio, photo) in enumerate(TEAM):
            member, created = TeamMember.objects.get_or_create(
                full_name=name,
                defaults=dict(
                    role=role,
                    group=group,
                    bio=f"<p>{bio}</p>" if bio else "",
                    short_bio=_summary(bio) if bio else "",
                    display_order=order,
                    is_published=True,
                ),
            )
            added += created
            if photo and self._needs_photo(member):
                source = PHOTO_DIR / f"{photo}.jpg"
                if source.exists():
                    with source.open("rb") as handle:
                        member.photo.save(f"{photo}.jpg", File(handle), save=True)
                    photos += 1
        self.stdout.write(
            f"  team: {len(TEAM)} listed, {added} added, {photos} photographs attached"
        )

    @staticmethod
    def _needs_photo(member):
        if not member.photo:
            return True
        try:
            return not member.photo.storage.exists(member.photo.name)
        except Exception:
            return False
