"""The site's main navigation.

Kept in one place so the desktop menu, the mobile drawer and the footer
cannot drift apart, and so the active item is decided once.
"""

from django.urls import reverse


# One icon per top-level item, for the mobile drawer.
ICONS = {
    "Home": "leaf",
    "About Us": "users",
    "Focus Areas": "sprout",
    "Programmes": "tree",
    "Resources": "file",
    "News": "calendar",
    "Gallery": "image",
    "Get Involved": "handshake",
    "Contact": "mail",
}


def build_nav(path: str):
    """Return the navigation tree, marking the branch the request is in."""
    items = [
        {"label": "Home", "url": reverse("site:home"), "children": []},
        {
            "label": "About Us",
            "url": reverse("site:about"),
            "children": [
                {"label": "Who We Are", "url": reverse("site:about")},
                {"label": "Vision & Mission", "url": reverse("site:about") + "#vision"},
                {"label": "Core Values", "url": reverse("site:about") + "#values"},
                {"label": "Our Objectives", "url": reverse("site:about") + "#objectives"},
                {"label": "Our Team", "url": reverse("site:team")},
            ],
        },
        {"label": "Focus Areas", "url": reverse("site:focus_areas"), "children": []},
        {
            "label": "Programmes",
            "url": reverse("site:programmes"),
            "children": [
                {"label": "All Programmes", "url": reverse("site:programmes")},
                {"label": "Ongoing", "url": reverse("site:programmes") + "?status=ongoing"},
                {"label": "Completed", "url": reverse("site:programmes") + "?status=completed"},
            ],
        },
        {"label": "Resources", "url": reverse("site:resources"), "children": []},
        {
            "label": "News",
            "url": reverse("site:news"),
            "children": [
                {"label": "News & Stories", "url": reverse("site:news")},
                {"label": "Events", "url": reverse("site:events")},
                {"label": "Announcements", "url": reverse("site:news") + "?kind=announcement"},
                {"label": "Impact Stories", "url": reverse("site:news") + "?kind=impact_story"},
                {"label": "Podcasts", "url": reverse("site:news") + "?kind=podcast"},
            ],
        },
        {
            "label": "Gallery",
            "url": reverse("site:gallery"),
            "children": [
                {"label": "Photos", "url": reverse("site:gallery")},
                {"label": "Videos", "url": reverse("site:videos")},
            ],
        },
        {
            "label": "Get Involved",
            "url": reverse("site:get_involved"),
            "children": [
                {"label": "Become a Volunteer", "url": reverse("site:volunteer")},
                {"label": "Partner With Us", "url": reverse("site:partner")},
                {"label": "Support Our Work", "url": reverse("site:donate")},
            ],
        },
        {"label": "Contact", "url": reverse("site:contact"), "children": []},
    ]

    for item in items:
        item["icon"] = ICONS.get(item["label"], "leaf")
        base = item["url"].split("?")[0].split("#")[0]
        if base == "/":
            item["active"] = path == "/"
        else:
            item["active"] = path == base or path.startswith(base.rstrip("/") + "/")
    return items
