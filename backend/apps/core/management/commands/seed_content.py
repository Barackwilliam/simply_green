"""Load the organisation's website content draft into the database.

Everything here comes from the client's "Official Website Content Draft One".
The command is idempotent: run it as often as you like, it updates in place
rather than duplicating. Editors can then refine any of it in the admin.
"""

from pathlib import Path

from django.conf import settings as django_settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.about.models import CoreValue, Objective, PartnerReason
from apps.core.models import HeroSlide, SiteSettings
from apps.programmes.models import FocusArea, Programme

CORE_VALUES = [
    (
        "Environmental Sustainability",
        "We promote responsible management, protection, restoration, and "
        "sustainable use of natural resources and ecosystems for present and "
        "future generations.",
        "leaf",
    ),
    (
        "Community Participation & Empowerment",
        "We believe communities are at the heart of lasting change. We promote "
        "meaningful participation, local ownership, and community-led solutions "
        "to environmental and social challenges.",
        "users",
    ),
    (
        "Integrity & Accountability",
        "We uphold transparency, ethical conduct, accountability, and "
        "responsible stewardship of the resources entrusted to us.",
        "shield-check",
    ),
    (
        "Inclusion & Equity",
        "We promote equal opportunities and meaningful participation for women, "
        "youth, vulnerable groups, and marginalized communities, ensuring that "
        "no one is left behind.",
        "scale",
    ),
    (
        "Innovation & Learning",
        "We encourage creativity, innovation, technology application, knowledge "
        "sharing, and continuous learning to develop practical solutions to "
        "environmental challenges.",
        "lightbulb",
    ),
    (
        "Partnership & Collaboration",
        "We work with communities, government institutions, the private sector, "
        "civil society organizations, development partners, and other "
        "stakeholders to build partnerships that create meaningful and lasting "
        "change.",
        "handshake",
    ),
]

OBJECTIVES = [
    "To promote environmental awareness and encourage community participation "
    "in protecting and conserving the environment.",
    "To support community initiatives aimed at improving waste management, "
    "reducing environmental pollution, and promoting cleaner surroundings.",
    "To empower young people, women, and local communities to participate in "
    "environmental conservation activities and sustainable environmental "
    "practices.",
    "To promote environmental education, knowledge sharing, and practical "
    "actions that encourage responsible use and protection of natural "
    "resources.",
    "To collaborate with relevant stakeholders in supporting environmental "
    "conservation and community-based environmental initiatives.",
]

FOCUS_AREAS = [
    (
        "Environmental Conservation",
        "We promote the protection, restoration, and sustainable management of "
        "natural resources and ecosystems. Through community-led conservation, "
        "environmental education, and practical action, we support healthier "
        "ecosystems and communities.",
        "tree",
    ),
    (
        "Climate Action",
        "We support communities to understand, prepare for, and respond to the "
        "impacts of climate change. Our work promotes climate awareness, "
        "resilience, adaptation, and locally driven solutions for a changing "
        "climate.",
        "cloud-sun",
    ),
    (
        "Waste Management",
        "We promote practical approaches to responsible waste management and "
        "pollution reduction. Through awareness, community engagement, and "
        "innovative solutions, we work towards cleaner, healthier, and more "
        "sustainable communities.",
        "recycle",
    ),
    (
        "Community Empowerment",
        "We put communities at the center of environmental action. We "
        "strengthen their capacity to identify challenges, influence decisions, "
        "and lead solutions that respond to local needs.",
        "users",
    ),
    (
        "Sustainable Livelihoods",
        "We connect environmental sustainability with economic opportunity. Our "
        "initiatives promote sustainable livelihood options that strengthen "
        "community resilience, support well-being, and create lasting value "
        "while protecting the environment.",
        "sprout",
    ),
    (
        "Research & Knowledge",
        "We generate, document, and share knowledge to better understand "
        "environmental and climate challenges. By connecting research with "
        "local knowledge and practical experience, we support evidence-based "
        "solutions and informed decision-making.",
        "search",
    ),
    (
        "Green Innovation",
        "We support innovative ideas, technologies, and approaches that address "
        "environmental challenges. Through green innovation, we promote "
        "practical solutions that can strengthen climate resilience, improve "
        "resource efficiency, and advance sustainable development.",
        "lightbulb",
    ),
]

PARTNER_REASONS = [
    (
        "Resource Stewardship & Financial Integrity",
        "We track every dollar and resource entrusted to us by our partners. "
        "Our transparent tracking systems ensure that all funding directly "
        "drives climate change resilience, environmental conservation and "
        "tangible community empowerment.",
        "scale",
    ),
    (
        "Grassroots Reach & Community Ownership",
        "We operate directly at the frontline with local communities. Our "
        "deep-rooted relationships with community members, women, and youth "
        "guarantee strong project ownership, high buy-in, and long-term "
        "sustainability.",
        "users",
    ),
    (
        "Alignment with Global & National Priorities",
        "We seamlessly align our grassroots projects with national "
        "environmental frameworks, corporate ESG criteria and UN Sustainable "
        "Development Goals (SDGs 5, 8, 12, 13, and 15) — delivering trackable "
        "metrics for donor compliance and sustainability reporting.",
        "globe",
    ),
    (
        "Governance & Institutional Compliance",
        "As a fully registered Tanzanian NGO, we maintain high standards of "
        "ethical leadership, regulatory compliance and regular impact reporting "
        "to safeguard our partners' investments.",
        "shield-check",
    ),
    (
        "Data-Driven & Innovative Solutions",
        "We combine grassroots experience with green innovation and "
        "evidence-based research. This enables us to design practical, scalable "
        "and adaptable solutions that respond directly to evolving climate and "
        "environmental challenges.",
        "trending-up",
    ),
]

PROGRAMMES = [
    {
        "title": "Jumuisha Initiative",
        "subtitle": "Inclusive school-based environmental education for students "
        "with special needs",
        "status": "ongoing",
        "location": "Ilala Municipal Council, Dar es Salaam",
        "region": "Dar es Salaam",
        "district": "Ilala",
        "beneficiaries": "Students with special needs, teachers and inclusive "
        "education units",
        "focus": ["Waste Management", "Community Empowerment", "Environmental Conservation"],
        "summary": "A school-based environmental programme promoting awareness, "
        "responsible waste management and inclusive participation among students "
        "with special needs in Dar es Salaam.",
        "body": (
            "<p>Jumuisha Initiative is a school-based environmental programme "
            "designed to promote environmental awareness, responsible waste "
            "management and inclusive participation among students with special "
            "needs in Dar es Salaam. The initiative recognizes that all students, "
            "regardless of their abilities or support requirements, should have an "
            "equal opportunity to understand environmental challenges and "
            "participate in practical actions that improve their school "
            "surroundings and the wider community.</p>"
            "<p>Through the project, we work with special schools and schools with "
            "inclusive education units within Ilala Municipal Council to strengthen "
            "students' knowledge and practical skills in waste separation, reuse, "
            "upcycling and environmental conservation. Learning is supported "
            "through demonstrations and hands-on activities, including the "
            "separation of organic waste, plastics, paper and other materials.</p>"
            "<p>Students are also introduced to safe and creative ways of reusing "
            "selected waste materials to make useful items such as plant pots, "
            "pencil holders, paper crafts and decorations.</p>"
            "<p>In general, the initiative seeks to build environmentally "
            "responsible schools in which students with special needs are "
            "recognised not only as beneficiaries, but also as active contributors "
            "to environmental solutions.</p>"
        ),
    },
    {
        "title": "Tandika Clean Market Initiative",
        "subtitle": "Best Practice Training, Environmental Leadership and "
        "Sustainable Waste Management Programme",
        "status": "ongoing",
        "location": "Tandika Market, Temeke, Dar es Salaam",
        "region": "Dar es Salaam",
        "district": "Temeke",
        "beneficiaries": "Market traders and market leadership",
        "focus": ["Waste Management", "Community Empowerment", "Sustainable Livelihoods"],
        "summary": "A community-based programme promoting improved waste "
        "management practices and a cleaner, healthier trading environment at "
        "Tandika Market in Temeke.",
        "body": (
            "<p>Tandika Clean Market Initiative is a community-based programme "
            "implemented by Simply Green Organization to promote improved waste "
            "management practices and a cleaner, healthier trading environment at "
            "Tandika Market in Temeke, Dar es Salaam. The initiative recognizes the "
            "important role markets play in local livelihoods and economic "
            "activity, while also addressing the environmental and public health "
            "challenges that arise when waste is not properly separated, stored and "
            "collected.</p>"
            "<p>The project focuses on strengthening the capacity of market traders "
            "to manage waste responsibly through practical training and "
            "demonstrations. Traders are supported to identify different types of "
            "waste generated through their daily business activities, separate "
            "organic waste from recyclable materials such as plastics, paper and "
            "metals, reduce unnecessary waste, reuse suitable materials and "
            "maintain clean trading areas. The training also covers safe waste "
            "handling, hygiene, appropriate temporary storage and the "
            "responsibilities of traders in maintaining a clean market.</p>"
            "<h2>Tandika Environmental Ambassadors</h2>"
            "<p>A key component of the initiative is the establishment of a Tandika "
            "Environmental Ambassadors Group comprising 20 market representatives. "
            "The ambassadors encourage proper waste separation, promote the correct "
            "use of waste containers, share environmental information with fellow "
            "traders, identify cleanliness challenges and maintain communication "
            "with market leadership.</p>"
            "<p>In general, this project seeks to encourage continued participation "
            "and make environmental responsibility part of the market's daily "
            "operations while also supporting the provision and appropriate "
            "placement of waste segregation containers, signs and other essential "
            "materials in selected market areas.</p>"
        ),
        "outcomes": [("Environmental Ambassadors trained", "20")],
    },
    {
        "title": "Mangrove Restoration and Management Project",
        "subtitle": "Community-led restoration, protection and sustainable "
        "livelihoods in Kijiji cha Wavuvi, Mtoni Ward, Temeke",
        "status": "ongoing",
        "location": "Kijiji cha Wavuvi, Mtoni Ward, Temeke, Dar es Salaam",
        "region": "Dar es Salaam",
        "district": "Temeke",
        "beneficiaries": "Coastal residents, women, young people and fishers",
        "focus": ["Environmental Conservation", "Climate Action", "Sustainable Livelihoods", "Research & Knowledge"],
        "summary": "Community-based restoration and long-term protection of "
        "mangrove forests at Kijiji cha Wavuvi, paired with livelihood options "
        "that make conservation worthwhile.",
        "body": (
            "<p>Mangrove Restoration and Management Project is a community-based "
            "programme implemented by Simply Green Organization to support the "
            "recovery and long-term protection of mangrove forests at Kijiji cha "
            "Wavuvi area, Mtoni Ward, Temeke, Dar es Salaam. The project recognizes "
            "the central role mangroves play in coastal protection, fisheries, "
            "carbon storage and biodiversity, as well as their importance to "
            "households whose livelihoods depend on coastal resources. It also "
            "responds to pressures from human activities and natural coastal "
            "processes that continue to affect mangrove areas along the Tanzanian "
            "coast.</p>"
            "<h2>Restoration that is measured by survival</h2>"
            "<p>Restoration is supported through the establishment of mangrove "
            "nurseries and the planting of ecologically appropriate species in "
            "suitable degraded areas. Restored sites are monitored over time, with "
            "attention to the survival and condition of planted mangroves and to "
            "natural regeneration, so that success is measured by lasting recovery "
            "and not by planting events alone.</p>"
            "<p>The project also works with residents and relevant authorities to "
            "strengthen the protection of existing mangrove forests through "
            "community monitoring, reporting of harmful activities and locally "
            "agreed conservation responsibilities.</p>"
            "<h2>Led by the people who live there</h2>"
            "<p>Residents, including women, young people and fishers, take part in "
            "identifying problems and restoration sites, contributing local "
            "knowledge, planting, monitoring and shaping arrangements for "
            "protecting restored areas. Community learning activities cover "
            "mangrove ecology, restoration, coastal pressures and responsible waste "
            "management, with involvement of schools and youth groups to build "
            "awareness among the next generation.</p>"
            "<h2>Livelihoods that reward conservation</h2>"
            "<p>The initiative also assesses environmentally appropriate livelihood "
            "options that can strengthen incentives for conservation, including "
            "beekeeping, crab farming and other locally suitable activities. Where "
            "an option is found to be feasible, a limited pilot is supported with "
            "selected community groups, accompanied by training in technical "
            "practices, business planning, record keeping, group governance and "
            "market access. Livelihood activities do not involve clearing mangroves "
            "or damaging sensitive habitats.</p>"
        ),
    },
]

WHO_WE_ARE = (
    "<p>Simply Green Organization (SGO) is a non-governmental organization "
    "registered in Tanzania under the Non-Governmental Organizations Act No. 24 "
    "of 2002, with Registration Number 00NGO/R5315. Established and registered "
    "in November 2023, SGO operates across Mainland Tanzania to promote "
    "environmental sustainability, climate action, community empowerment, and "
    "sustainable livelihoods.</p>"
    "<p>SGO works closely with communities, particularly women, youth, and other "
    "vulnerable groups to address environmental challenges, strengthen "
    "resilience and create opportunities for sustainable development.</p>"
    "<p>The organization delivers its work through environmental conservation, "
    "climate change awareness, community engagement, innovation, research, "
    "partnerships, and practical, community-driven solutions that contribute to "
    "sustainable development and a resilient future for Tanzania.</p>"
)


ASSET_DIR = Path(django_settings.BASE_DIR).parent / "assets" / "source"

# Which supplied photograph illustrates which programme.
PROGRAMME_IMAGES = {
    "Jumuisha Initiative": "planning-session.jpg",
    "Tandika Clean Market Initiative": "tying-waste-sacks.jpg",
    "Mangrove Restoration and Management Project": "litter-collection.jpg",
}


def attach_image(instance, field_name, filename, *, force=False):
    """Attach a file from assets/source to an ImageField.

    Skips silently when the source is missing, and leaves an existing
    upload alone unless `force` is set — so re-running the command never
    overwrites an image an editor has since replaced.

    "Existing" means the file is actually there, not merely that the
    column holds a path. On a host with no persistent disk the database
    survives a deploy and the uploads do not, and this check only looked
    at the column: it saw a path, concluded the image was present, and
    left the site pointing at files that had been wiped. Every photograph
    on the production site was a 404 for exactly this reason.
    """
    field = getattr(instance, field_name)
    if field and not force:
        try:
            if field.storage.exists(field.name):
                return False
        except Exception:
            # If the backend cannot answer, assume it is there rather than
            # overwrite something real.
            return False

    source = ASSET_DIR / filename
    if not source.exists():
        return False

    with source.open("rb") as handle:
        field.save(filename, File(handle), save=True)
    return True


class Command(BaseCommand):
    help = "Load the client's website content draft into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Overwrite records that already exist. Without this the "
                "command only fills in what is missing, so it is safe to run "
                "on every deploy without undoing an editor's changes."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.force = options["force"]
        self._site_settings()
        self._core_values()
        self._objectives()
        self._partner_reasons()
        focus_by_title = self._focus_areas()
        self._programmes(focus_by_title)
        self._hero_slides()
        self.stdout.write(self.style.SUCCESS("Content draft loaded."))

    def _upsert(self, model, defaults, **lookup):
        """Create when missing; update only when --force was passed."""
        if self.force:
            return model.objects.update_or_create(defaults=defaults, **lookup)
        return model.objects.get_or_create(defaults=defaults, **lookup)

    def _site_settings(self):
        settings_obj = SiteSettings.load()
        if settings_obj.vision and not self.force:
            # The words are the editor's now, but the logo file may still
            # have been wiped with the disk, and attach_image only acts
            # when the file is genuinely missing.
            if attach_image(settings_obj, "logo", "logo.png"):
                self.stdout.write("  logo restored")
            self.stdout.write("  site settings already filled in — left alone")
            return
        settings_obj.organisation_name = "Simply Green Organization"
        settings_obj.acronym = "SGO"
        settings_obj.tagline = (
            "A greener, more resilient Tanzania — led by its own communities"
        )
        settings_obj.registration_number = "00NGO/R5315"
        settings_obj.registration_statement = (
            "Simply Green Organization is registered in Tanzania under the "
            "Non-Governmental Organizations Act No. 24 of 2002, Registration "
            "Number 00NGO/R5315, and has operated across Mainland Tanzania "
            "since November 2023."
        )
        settings_obj.vision = (
            "We envision communities that are better equipped to protect their "
            "environment, respond to climate challenges, adopt sustainable "
            "practices and contribute to a greener and more resilient Tanzania."
        )
        settings_obj.mission = (
            "To empower communities to protect the environment and address "
            "climate challenges through sustainable conservation practices, "
            "innovation, and livelihood initiatives that contribute to "
            "sustainable development."
        )
        settings_obj.who_we_are = WHO_WE_ARE
        settings_obj.city = "Dar es Salaam"
        settings_obj.country = "Tanzania"
        settings_obj.default_meta_title = (
            "Simply Green Organization — Environmental action in Tanzania"
        )
        settings_obj.default_meta_description = (
            "Simply Green Organization empowers communities across Tanzania to "
            "protect the environment, respond to climate change and build "
            "sustainable livelihoods."
        )
        settings_obj.save()
        if attach_image(settings_obj, "logo", "logo.png"):
            self.stdout.write("  logo uploaded")
        self.stdout.write("  site settings")

    def _core_values(self):
        for order, (title, description, icon) in enumerate(CORE_VALUES):
            self._upsert(
                CoreValue,
                {"description": description, "icon": icon, "display_order": order},
                title=title,
            )
        self.stdout.write(f"  core values ({len(CORE_VALUES)})")

    def _objectives(self):
        for order, text in enumerate(OBJECTIVES):
            self._upsert(Objective, {"display_order": order}, text=text)
        self.stdout.write(f"  objectives ({len(OBJECTIVES)})")

    def _partner_reasons(self):
        for order, (title, description, icon) in enumerate(PARTNER_REASONS):
            self._upsert(
                PartnerReason,
                {"description": description, "icon": icon, "display_order": order},
                title=title,
            )
        self.stdout.write(f"  partner reasons ({len(PARTNER_REASONS)})")

    def _focus_areas(self):
        mapping = {}
        for order, (title, summary, icon) in enumerate(FOCUS_AREAS):
            area, _ = self._upsert(
                FocusArea,
                {"summary": summary, "icon": icon, "display_order": order},
                title=title,
            )
            mapping[title] = area
        self.stdout.write(f"  focus areas ({len(FOCUS_AREAS)})")
        return mapping

    def _hero_slides(self):
        slides = [
            {
                "image": "team-with-collected-waste.jpg",
                "alt": "Simply Green Organization staff with sacks of waste "
                       "collected at a coastal clean-up in Dar es Salaam",
                "eyebrow": "Registered NGO · Tanzania",
                "headline": "A greener, more resilient Tanzania — led by its "
                            "own communities",
                "sub": "We empower communities to protect the environment and "
                       "address climate challenges through conservation, "
                       "innovation and sustainable livelihoods.",
                "p_label": "See our programmes", "p_url": "/programmes/",
                "s_label": "Get involved", "s_url": "/get-involved/",
            },
            {
                "image": "litter-collection.jpg",
                "alt": "Team members clearing plastic waste from a shoreline",
                "eyebrow": "Waste management",
                "headline": "Cleaner markets, cleaner coastlines",
                "sub": "From Tandika Market to the shoreline at Mtoni, we work "
                       "with traders, schools and households to separate, "
                       "reduce and reuse what would otherwise be dumped.",
                "p_label": "How we work", "p_url": "/focus-areas/",
                "s_label": "Volunteer with us", "s_url": "/get-involved/volunteer/",
            },
            {
                "image": "planning-session.jpg",
                "alt": "Simply Green Organization team planning a programme",
                "eyebrow": "Partner with us",
                "headline": "Grassroots reach, accounted for to the shilling",
                "sub": "We work at the frontline with communities, and we "
                       "report transparently against national frameworks and "
                       "the Sustainable Development Goals.",
                "p_label": "Partner with us", "p_url": "/get-involved/partner/",
                "s_label": "Support our work", "s_url": "/donate/",
            },
        ]
        for order, entry in enumerate(slides):
            slide, created = self._upsert(
                HeroSlide,
                {
                    "image_alt": entry["alt"],
                    "eyebrow": entry["eyebrow"],
                    "subheadline": entry["sub"],
                    "primary_label": entry["p_label"],
                    "primary_url": entry["p_url"],
                    "secondary_label": entry["s_label"],
                    "secondary_url": entry["s_url"],
                    "display_order": order,
                },
                headline=entry["headline"],
            )
            attach_image(slide, "image", entry["image"])
        self.stdout.write(f"  home page slides ({len(slides)})")

    def _programmes(self, focus_by_title):
        from apps.programmes.models import ProgrammeOutcome

        for order, entry in enumerate(PROGRAMMES):
            programme, _ = self._upsert(
                Programme,
                {
                    "subtitle": entry["subtitle"],
                    "status": entry["status"],
                    "summary": entry["summary"],
                    "body": entry["body"],
                    "location": entry["location"],
                    "region": entry["region"],
                    "district": entry["district"],
                    "beneficiaries": entry["beneficiaries"],
                    "display_order": order,
                    "is_featured": True,
                },
                title=entry["title"],
            )
            programme.focus_areas.set(
                [focus_by_title[name] for name in entry["focus"]]
            )
            image_name = PROGRAMME_IMAGES.get(entry["title"])
            if image_name:
                attach_image(programme, "featured_image", image_name)

            for outcome_order, (label, value) in enumerate(
                entry.get("outcomes", [])
            ):
                self._upsert(
                    ProgrammeOutcome,
                    {"value": value, "display_order": outcome_order},
                    programme=programme,
                    label=label,
                )
        self.stdout.write(f"  programmes ({len(PROGRAMMES)})")
