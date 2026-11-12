"""The organisation's journey and the Sustainable Development Goals it
works toward, for the home and about pages.

Kept here rather than in the database because they change rarely and
only with the organisation's say-so; every line is a fact from the
registration, the photo albums or the programmes, not a placeholder.
"""

from django.urls import reverse


def journey():
    return [
        {
            "when": "November 2023",
            "title": "Registered as a national NGO",
            "text": "Simply Green Organization is registered under the "
                    "Non-Governmental Organizations Act No. 24 of 2002 "
                    "(Reg. No. 00NGO/R5315) and begins work across Mainland "
                    "Tanzania.",
        },
        {
            "when": "2024",
            "title": "Circular Economy Workshop",
            "text": "Producers, recyclers, government and civil society meet "
                    "to discuss extended producer responsibility and a "
                    "circular economy for Tanzania.",
            "url": reverse("site:album_detail", kwargs={"slug": "circular-economy-workshop-2024"}),
        },
        {
            "when": "November 2024",
            "title": "Rainbow Beach clean-up, Mbezi",
            "text": "Volunteers, partners and neighbours clear plastic from "
                    "Rainbow Beach in Kinondoni under the message “Keep our "
                    "ocean clean”.",
            "url": reverse("site:album_detail", kwargs={"slug": "rainbow-beach-clean-up-mbezi"}),
        },
        {
            "when": "March 2025",
            "title": "Kawe clean-up and waste audit",
            "text": "A morning on the Kawe shoreline, ending with an audit of "
                    "everything collected to show where the waste comes from.",
            "url": reverse("site:album_detail", kwargs={"slug": "kawe-beach-clean-up"}),
        },
        {
            "when": "Today",
            "title": "Schools, markets and mangroves",
            "text": "Jumuisha in Ilala schools, the Tandika Clean Market "
                    "Initiative in Temeke and mangrove restoration at Mtoni.",
            "url": reverse("site:programmes"),
        },
    ]


# The official SDG colours. White text fails contrast on the lighter ones,
# so each carries the ink its label is set in.
SDGS = [
    {"n": 5, "name": "Gender equality", "color": "#FF3A21", "ink": "#ffffff",
     "text": "Women, youth and vulnerable groups at the centre of "
             "environmental action and of the decisions about it."},
    {"n": 8, "name": "Decent work and economic growth", "color": "#A21942", "ink": "#ffffff",
     "text": "Livelihood options that tie caring for the environment to "
             "an income."},
    {"n": 12, "name": "Responsible consumption and production", "color": "#BF8B2E", "ink": "#1d1405",
     "text": "Waste audits, cleaner markets and a circular economy that "
             "cut waste at the source."},
    {"n": 13, "name": "Climate action", "color": "#3F7E44", "ink": "#ffffff",
     "text": "Helping communities understand, prepare for and respond to "
             "climate change."},
    {"n": 15, "name": "Life on land", "color": "#56C02B", "ink": "#0f2a06",
     "text": "Protecting, restoring and sustainably managing ecosystems, "
             "mangroves among them."},
]
