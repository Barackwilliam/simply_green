"""Load placeholder content so the design can be reviewed before the client
sends theirs.

Several sections of the site render nothing at all when their table is
empty — impact figures, team, news, events, the gallery, the resource
centre. That makes the site impossible to judge and impossible to show to
the client. This command fills those sections with clearly provisional
content so the layout can be seen end to end.

None of it is real. The figures are invented, the people do not exist and
the articles describe nothing that happened. While any of it is loaded the
footer carries a line saying so, so nobody reading the site mistakes it for
the organisation's own record.

Kept well away from ``seed_content``, which carries the client's actual
draft. This one is never part of the build unless it is switched on, and
everything it creates comes out again with ``--remove``:

    python manage.py seed_sample_content
    python manage.py seed_sample_content --remove

On Render there is no shell on the free plan, so the build runs
``--if-enabled`` instead and the SAMPLE_CONTENT environment variable
decides: "on" loads it, "off" takes it out again, unset does nothing.
"""

import os
from pathlib import Path

from django.conf import settings as django_settings
from django.core.cache import cache
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.about.models import TeamMember
from apps.core.models import ImpactStat
from apps.gallery.models import Album, Photo
from apps.news.models import Category, Event, Post
from apps.resources.models import Publication

ASSET_DIR = Path(django_settings.BASE_DIR).parent / "assets" / "source"

# Marks every row this command owns. Nothing without it is ever touched,
# so --remove cannot reach a record the client has since added by hand.
MARK = "[sample]"

STATS = [
    ("Trees planted with communities", "48,200", "+", "sprout"),
    ("Tonnes of waste collected", "1,340", "", "recycle"),
    ("People reached directly", "26,500", "+", "users"),
    ("Schools running green clubs", "72", "", "lightbulb"),
]

TEAM = [
    (
        "Amina Mwakalinga",
        "Executive Director",
        "leadership",
        "Leads strategy and partnerships, and has run coastal clean-up "
        "programmes since 2014.",
    ),
    (
        "Joseph Kibona",
        "Programmes Manager",
        "leadership",
        "Plans and runs field operations across Dar es Salaam, Pwani and "
        "Morogoro.",
    ),
    (
        "Neema Shayo",
        "Community Engagement Lead",
        "staff",
        "Builds the school and ward-level green clubs that carry the work "
        "locally.",
    ),
    (
        "Daniel Mushi",
        "Monitoring & Reporting Officer",
        "staff",
        "Keeps the numbers honest — every tree, tonne and training day is "
        "recorded.",
    ),
    (
        "Grace Lyimo",
        "Finance & Administration",
        "staff",
        "Runs procurement, payroll and the grant reporting calendar.",
    ),
    (
        "Dr. Hamisi Juma",
        "Board Chairperson",
        "board",
        "Environmental scientist, twenty years in coastal ecosystem research.",
    ),
    (
        "Rehema Ngowi",
        "Board Member",
        "board",
        "Community development specialist focused on women's livelihoods.",
    ),
]

# (title, excerpt, body paragraphs, kind, days ago, asset image)
# Reading time is computed from the body on save, so these carry enough
# text for an article page to be worth looking at rather than a stub.
POSTS = [
    (
        "1,200 mangrove seedlings go in at Mbweni",
        "Three wards planted together over one weekend, and the ward "
        "environment committee has taken on the watering rota.",
        [
            "Over two days in October, volunteers from three wards put 1,200 "
            "mangrove seedlings into the tidal flats north of Mbweni. The "
            "planting had been three months in preparation: the nursery was "
            "raised locally, the site was mapped with the ward environment "
            "committee, and the planting lines were set out against the tide "
            "rather than against the road.",
            "Mangroves are the cheapest coastal defence there is. A healthy "
            "stand slows a storm surge before it reaches the houses behind "
            "it, holds sediment that would otherwise wash out, and gives the "
            "fishery somewhere to breed. Where the stand has gone, all three "
            "of those go with it, and the households that notice first are "
            "the ones with the least room to absorb the loss.",
            "What matters now is the next eighteen months. Seedlings fail "
            "when nobody is responsible for them, so the ward environment "
            "committee has taken on the watering and replacement rota and "
            "will report survival counts each quarter. We will publish those "
            "counts here, including the ones we would rather not.",
            "Thanks go to the ward leadership, to the nursery group who "
            "raised the seedlings, and to every volunteer who spent a "
            "weekend up to their knees in mud.",
        ],
        "impact_story",
        5,
        "litter-collection.jpg",
    ),
    (
        "Green clubs now reach 72 schools",
        "What began in four classrooms is now a termly programme with its "
        "own pupil-led monitoring sheets.",
        [
            "The school green club programme started in 2022 with four "
            "classrooms and a single question: what happens to the waste "
            "that leaves this compound? Seventy-two schools later, the "
            "question has not changed, but the pupils answering it now keep "
            "their own records.",
            "Each club runs a termly waste audit. Pupils weigh what the "
            "school throws out, sort it into what can be composted, what can "
            "be sold on and what has nowhere to go, and write the figures up "
            "on a sheet that stays on the wall. The sheet is the point: a "
            "number a child wrote down themselves is argued about in a way "
            "that a number from a visitor never is.",
            "Teachers tell us the second-order effects are the bigger ones. "
            "Composting changed what the school garden could grow. Sorting "
            "changed what the tuck shop was willing to stock. In eleven "
            "schools the club has taken its figures to the ward office and "
            "asked for a collection point.",
            "Next term the programme extends to a further twenty schools in "
            "Temeke and Kigamboni, with the monitoring sheets translated and "
            "printed locally so that no club has to wait on us for paper.",
        ],
        "news",
        14,
        "planning-session.jpg",
    ),
    (
        "A cleaner Msimbazi starts upstream",
        "Waste reaching the valley traces back to five collection points — "
        "and fixing those five changed the river.",
        [
            "For years the response to waste in the Msimbazi valley was to "
            "clear what had already arrived. It is visible work and it feels "
            "productive, and within a fortnight the valley looks exactly as "
            "it did before. We spent six months asking a different question: "
            "where is it coming in?",
            "The answer was narrower than anyone expected. Tracking waste "
            "flows across the catchment, five collection points accounted "
            "for the overwhelming majority of what ended up in the river. "
            "Each was overflowing on a predictable schedule, and each sat "
            "close enough to a drainage line that one heavy rain did the "
            "rest.",
            "Working with the ward offices, those five points now have "
            "scheduled collection and enclosed storage. The clearing teams "
            "still go out, but they are no longer emptying a bath with the "
            "tap running. Volume recovered downstream has fallen sharply "
            "across the last two quarters.",
            "The method matters more than the result. Mapping a catchment "
            "before clearing it is slower, less photogenic, and considerably "
            "cheaper than doing the same clean-up every month for a decade. "
            "The full assessment is in the resource centre.",
        ],
        "impact_story",
        28,
        "team-with-collected-waste.jpg",
    ),
    (
        "Training 40 women in briquette production",
        "Turning agricultural waste into cooking fuel cuts both charcoal "
        "spending and the pressure on nearby woodland.",
        [
            "Forty women from two wards completed a four-day course in "
            "briquette production this month, covering feedstock selection, "
            "carbonisation, binding, pressing and drying, along with costing "
            "and basic record keeping.",
            "The feedstock is agricultural residue that is currently burned "
            "in the field — maize cobs, rice husks, sawdust from the nearby "
            "timber yards. Compressed into briquettes it burns longer and "
            "cleaner than the charcoal most households buy, at a lower cost "
            "per meal cooked.",
            "Two things follow from that. Household fuel spending falls, "
            "which matters most in the homes where it is the largest "
            "discretionary line. And demand for charcoal falls, which takes "
            "pressure off woodland that is already thinner than it was a "
            "decade ago.",
            "Each participant leaves with a press, a starter stock of binder "
            "and a costing sheet. Six have already formed a production group "
            "and are supplying two local restaurants. We will follow the "
            "cohort for a year and publish what we find, including how many "
            "are still producing at the end of it.",
        ],
        "news",
        41,
        "tying-waste-sacks.jpg",
    ),
    (
        "Annual report 2025 is out",
        "Every shilling, every site and every partner from the past twelve "
        "months, in one document.",
        [
            "Our annual report for 2025 is now available in the resource "
            "centre. It covers every programme we ran, every site we worked "
            "on, and every shilling that passed through the organisation.",
            "The report is deliberately detailed. Expenditure is broken down "
            "by programme and by category rather than presented as a single "
            "pie chart, the independent auditor's statement is reproduced in "
            "full, and each programme carries its own targets alongside what "
            "was actually achieved — including where we fell short.",
            "Two things did not go to plan this year, and both are written "
            "up rather than left out. A nursery site was lost to flooding in "
            "March, and one school cohort was delayed a full term by a "
            "staffing change on our side.",
            "If you are considering funding this work, this is the document "
            "to read first. If something in it is unclear, write to us and "
            "we will answer.",
        ],
        "announcement",
        60,
        "team-portrait.jpg",
    ),
]

# (title, days ahead, venue, online)
EVENTS = [
    ("Coastal clean-up: Coco Beach", 6, "Coco Beach, Dar es Salaam", False),
    ("Tree planting day: Pugu Hills", 20, "Pugu Forest Reserve", False),
    ("Webinar: community waste economics", 33, "", True),
    ("Schools green club festival", 48, "Mnazi Mmoja Grounds", False),
]

ALBUMS = [
    (
        "Mbweni mangrove planting",
        "A weekend of planting with three ward committees.",
        12,
        "Mbweni, Dar es Salaam",
        [
            ("litter-collection.jpg", "Collecting waste along the shoreline"),
            ("team-with-collected-waste.jpg", "Sacks ready for the collection point"),
            ("tying-waste-sacks.jpg", "Tying off a full sack"),
        ],
    ),
    (
        "Community planning sessions",
        "Ward committees setting their own targets for the season.",
        46,
        "Temeke, Dar es Salaam",
        [
            ("planning-session.jpg", "A ward planning session in progress"),
            ("team-portrait.jpg", "The team after the session"),
        ],
    ),
]

# (title, kind, year, summary, pages)
PUBLICATIONS = [
    (
        "Annual Report 2025",
        "annual_report",
        2025,
        "Programmes, reach and expenditure for the year, with site-by-site "
        "figures and the independent auditor's statement.",
        48,
    ),
    (
        "Msimbazi waste flow assessment",
        "research",
        2025,
        "Where the waste reaching the valley actually comes from, traced "
        "across five collection points over six months.",
        22,
    ),
    (
        "Strategic Plan 2025–2029",
        "strategic_plan",
        2025,
        "The four priorities for the next five years and how progress "
        "against each will be measured.",
        31,
    ),
]


class Command(BaseCommand):
    help = (
        "Load clearly-labelled placeholder content so the design can be "
        "reviewed before the client's own content arrives."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--remove",
            action="store_true",
            help="Delete everything this command created and nothing else.",
        )
        parser.add_argument(
            "--if-enabled",
            action="store_true",
            help=(
                "Read the SAMPLE_CONTENT environment variable instead: 'on' "
                "loads, 'off' removes, anything else does nothing. For the "
                "build command, where there is no shell to run this by hand."
            ),
        )

    def handle(self, *args, **options):
        remove = options["remove"]

        if options["if_enabled"]:
            flag = os.environ.get("SAMPLE_CONTENT", "").strip().lower()
            if flag in {"on", "1", "true", "yes"}:
                remove = False
            elif flag in {"off", "0", "false", "no"}:
                remove = True
            else:
                self.stdout.write("SAMPLE_CONTENT not set — nothing to do.")
                return

        if remove:
            self._remove()
        else:
            self._load()
        # The footer notice is read from a cached flag; without this it
        # keeps saying the opposite of the truth for the next five minutes.
        cache.delete("sample-content")

    # -- loading ---------------------------------------------------------

    @transaction.atomic
    def _load(self):
        self._stats()
        self._team()
        posts = self._posts()
        self._events()
        self._albums()
        self._publications()

        self.stdout.write(
            self.style.WARNING(
                "\nSample content loaded. None of it is real — the figures "
                "are invented and the people named do not exist. The footer "
                "says so while it is in place. Take it out with:\n"
                "    python manage.py seed_sample_content --remove\n"
            )
        )
        self.stdout.write(f"  {len(posts)} articles, and the rest alongside.")

    def _attach(self, instance, field_name, filename):
        """Attach an asset, leaving an existing upload alone.

        "Existing" means the file is really there. A column holding a path
        to a file the disk no longer has is not an image, and treating it
        as one is what left the deployed site showing nothing but broken
        pictures after a redeploy.
        """
        field = getattr(instance, field_name)
        if field:
            try:
                if field.storage.exists(field.name):
                    return
            except Exception:
                return
        source = ASSET_DIR / filename
        if not source.exists():
            self.stdout.write(f"  missing asset, skipped: {filename}")
            return
        with source.open("rb") as handle:
            field.save(f"{instance.pk}-{filename}", File(handle), save=True)

    def _stats(self):
        for order, (label, value, suffix, icon) in enumerate(STATS):
            ImpactStat.objects.update_or_create(
                label=label,
                defaults=dict(
                    value=value,
                    suffix=suffix,
                    icon=icon,
                    description=MARK,
                    display_order=order,
                    is_published=True,
                ),
            )
        self.stdout.write(f"  impact figures ({len(STATS)})")

    def _team(self):
        # No photographs. The only people pictures to hand are group shots of
        # a clean-up; using one as four different staff portraits would be a
        # lie about who these people are. The card falls back to an initial
        # on a gradient, which reads as deliberate.
        for order, (name, role, group, bio) in enumerate(TEAM):
            TeamMember.objects.update_or_create(
                full_name=name,
                defaults=dict(
                    role=role,
                    group=group,
                    short_bio=bio,
                    bio=f"<p>{bio}</p>",
                    display_order=order,
                    is_published=True,
                ),
            )
        self.stdout.write(f"  team members ({len(TEAM)}), no photographs")

    def _posts(self):
        category, _ = Category.objects.get_or_create(
            name="Field notes",
            defaults=dict(description=MARK, is_published=True),
        )
        created = []
        for title, excerpt, paragraphs, kind, days, asset in POSTS:
            # reading_minutes is derived from the body on save, so it is not
            # set here — it would only be overwritten.
            post, _ = Post.objects.update_or_create(
                title=title,
                defaults=dict(
                    excerpt=excerpt,
                    body="".join(f"<p>{para}</p>" for para in paragraphs),
                    kind=kind,
                    category=category,
                    published_at=timezone.now() - timezone.timedelta(days=days),
                    is_published=True,
                ),
            )
            self._attach(post, "featured_image", asset)
            if not post.featured_image_alt:
                post.featured_image_alt = (
                    "Simply Green Organization volunteers at work"
                )
                post.save(update_fields=["featured_image_alt"])
            created.append(post)
        self.stdout.write(f"  articles ({len(created)})")
        return created

    def _events(self):
        for title, days, venue, online in EVENTS:
            Event.objects.update_or_create(
                title=title,
                defaults=dict(
                    summary=(
                        "Open to everyone. Bring water, gloves and closed "
                        "shoes; tools and refreshments are provided."
                        if not online
                        else "An hour online, with time for questions at the end."
                    ),
                    venue=venue,
                    is_online=online,
                    status="upcoming",
                    start_datetime=timezone.now() + timezone.timedelta(days=days),
                    is_published=True,
                ),
            )
        self.stdout.write(f"  events ({len(EVENTS)})")

    def _albums(self):
        for order, (title, description, days, location, photos) in enumerate(ALBUMS):
            album, _ = Album.objects.update_or_create(
                title=title,
                defaults=dict(
                    description=description,
                    location=location,
                    date=(timezone.now() - timezone.timedelta(days=days)).date(),
                    display_order=order,
                    is_published=True,
                ),
            )
            self._attach(album, "cover_image", photos[0][0])
            for i, (asset, caption) in enumerate(photos):
                source = ASSET_DIR / asset
                if not source.exists():
                    continue
                # A row whose file the disk no longer has is not a
                # photograph. Reuse the row and give it its picture back
                # rather than skipping it and leaving a broken image.
                photo = album.photos.filter(caption=caption).first()
                if photo and photo.image:
                    try:
                        if photo.image.storage.exists(photo.image.name):
                            continue
                    except Exception:
                        continue
                if photo is None:
                    photo = Photo(
                        album=album, caption=caption, alt_text=caption,
                        display_order=i,
                    )
                with source.open("rb") as handle:
                    photo.image.save(f"{album.slug}-{i}-{asset}", File(handle), save=True)
        self.stdout.write(f"  albums ({len(ALBUMS)})")

    def _publications(self):
        # No files. A download button on a document that does not exist is
        # worse than no button; the template already hides it.
        for order, (title, kind, year, summary, pages) in enumerate(PUBLICATIONS):
            Publication.objects.update_or_create(
                title=title,
                defaults=dict(
                    kind=kind,
                    year=year,
                    summary=summary,
                    page_count=pages,
                    published_date=timezone.datetime(year, 3, 1).date(),
                    display_order=order,
                    is_published=True,
                ),
            )
        self.stdout.write(f"  publications ({len(PUBLICATIONS)}), no files attached")

    # -- removal ---------------------------------------------------------

    @transaction.atomic
    def _remove(self):
        counts = []

        counts.append(
            ("impact figures", ImpactStat.objects.filter(
                label__in=[s[0] for s in STATS]).delete()[0])
        )
        counts.append(
            ("team members", TeamMember.objects.filter(
                full_name__in=[t[0] for t in TEAM]).delete()[0])
        )
        counts.append(
            ("articles", Post.objects.filter(
                title__in=[p[0] for p in POSTS]).delete()[0])
        )
        counts.append(
            ("events", Event.objects.filter(
                title__in=[e[0] for e in EVENTS]).delete()[0])
        )
        # Photos go with the album, by cascade.
        counts.append(
            ("albums", Album.objects.filter(
                title__in=[a[0] for a in ALBUMS]).delete()[0])
        )
        counts.append(
            ("publications", Publication.objects.filter(
                title__in=[p[0] for p in PUBLICATIONS]).delete()[0])
        )
        # Only if nothing else was filed under it in the meantime.
        counts.append(
            ("category", Category.objects.filter(
                name="Field notes", description=MARK, posts__isnull=True).delete()[0])
        )

        for label, n in counts:
            self.stdout.write(f"  {label}: {n} rows removed")
        self.stdout.write(self.style.SUCCESS("Sample content removed."))
