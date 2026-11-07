"""One breadcrumb trail per page, derived from the url.

The trail was written out by hand in each of twenty templates, with three
different conventions — "Home / About Us", "Get Involved / Donate", and a
bare back-link on the detail pages. None of it reached a search engine,
because none of it was marked up.

Deriving it from the path means the visible trail and the BreadcrumbList
that Google reads can never disagree, and a page added later gets both
without anyone remembering to.
"""

from django.urls import NoReverseMatch, reverse

# Path segment -> what to call it, for the segments that are not a page in
# their own right or whose title is not the slug with the hyphens removed.
LABELS = {
    "about": "About Us",
    "team": "Our Team",
    "focus-areas": "Focus Areas",
    "programmes": "Programmes",
    "resources": "Resource Centre",
    "news": "News & Stories",
    "events": "Events",
    "gallery": "Gallery",
    "videos": "Videos",
    "get-involved": "Get Involved",
    "volunteer": "Volunteer",
    "partner": "Partner With Us",
    "donate": "Donate",
    "contact": "Contact",
    "privacy": "Privacy",
}

# Segments that exist only to group urls and have no page behind them.
NOT_A_PAGE = set()


def trail(path, final=None):
    """[{name, url, last}] from "/" to the current page.

    `final` names the last crumb when it cannot be read off the url — an
    article's title rather than its slug.
    """
    crumbs = [{"name": "Home", "url": "/", "last": False}]

    parts = [p for p in (path or "/").strip("/").split("/") if p]
    walked = ""
    for index, part in enumerate(parts):
        walked += "/" + part
        is_last = index == len(parts) - 1
        if is_last and final:
            name = final
        else:
            name = LABELS.get(part) or part.replace("-", " ").capitalize()
        crumbs.append({
            "name": name,
            "url": walked + "/",
            "last": is_last,
            "linked": not is_last and part not in NOT_A_PAGE,
        })

    if len(crumbs) == 1:
        # The home page is not its own breadcrumb.
        return []
    crumbs[0]["linked"] = True
    return crumbs


def home_url():
    try:
        return reverse("site:home")
    except NoReverseMatch:  # pragma: no cover
        return "/"
