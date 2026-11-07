"""Responsive picture markup.

One tag, used everywhere a photograph is shown, so that the decisions about
srcset, sizes, lazy loading, dimensions and focal point are made once rather
than copied across twenty templates and then drifting apart.

    {% picture post.featured_image alt=post.title sizes=CARD_SIZES %}

What it writes, when renditions exist:

    <picture>
      <source type="image/webp" srcset="…-420.webp 420w, …-760.webp 760w" sizes="…">
      <img src="…master.jpg" width="1800" height="1350" alt="…"
           loading="lazy" decoding="async" style="object-position:50% 38%">
    </picture>

and a plain <img> when they do not, which is always correct and merely
heavier — a page must never break because the pipeline has not caught up.
"""

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from apps.core.renditions import lookup, present

register = template.Library()

# Named so templates read as intent rather than as arithmetic. Each says how
# wide the image will be painted, which is what the browser needs in order to
# pick a width from the srcset before any CSS has been applied.
SIZES = {
    # Full width always: hero, photo bands.
    "full": "100vw",
    # Three to a row on a desktop, one on a phone.
    "card": "(max-width: 620px) 100vw, (max-width: 1040px) 48vw, 400px",
    # Four to a row: team portraits.
    "quarter": "(max-width: 420px) 100vw, (max-width: 800px) 48vw, (max-width: 1040px) 31vw, 290px",
    # Half the page: the side-by-side text-and-photo sections.
    "half": "(max-width: 900px) 100vw, 560px",
    # A carousel item.
    "slide": "(max-width: 900px) 78vw, 430px",
}


def _static_fallback(path, alt, css, priority, ratio, style):
    """The bundled stand-in, when there is no usable upload."""
    if not path:
        return ""
    from django.templatetags.static import static

    attrs = [
        f'src="{escape(static(path))}"',
        f'alt="{escape(alt or "")}"',
        'decoding="async"',
    ]
    if css:
        attrs.append(f'class="{escape(css)}"')
    attrs.append('fetchpriority="high"' if priority else 'loading="lazy"')
    inline = []
    if ratio:
        inline.append(f"aspect-ratio:{ratio}")
    if style:
        inline.append(style.rstrip(";"))
    if inline:
        attrs.append(f'style="{escape(";".join(inline))}"')
    return mark_safe(f"<img {' '.join(attrs)}>")


@register.simple_tag
def picture(
    image,
    alt="",
    sizes="card",
    css="",
    loading="lazy",
    priority=False,
    ratio=None,
    style="",
    deferred=False,
    fallback="",
):
    """Render one photograph at the sizes the layout will actually use.

    `sizes` takes a key from SIZES above, or a raw sizes attribute.
    `priority` marks the one image that is visible before any scrolling —
    there should be at most one per page, and it is never lazy.

    `fallback` is a path under static/ to use when the upload is not
    there. Static files live in the repository and are served by
    WhiteNoise, so they survive a deploy whatever happens to the media
    disk — which on this host is everything.

    `deferred` writes the urls into data- attributes instead, for images
    the page must not fetch on load at all. loading="lazy" cannot do this
    job for a carousel slide: a slide that is merely transparent still
    counts as being in the viewport, so the browser fetches it anyway.
    Something has to move the attributes across later, and for the hero
    that is the slideshow script.
    """
    if not image or not present(image):
        # A column holding a path to a file that is gone is not an image.
        # Rendering it anyway is how every page on the deployed site came
        # to show a broken picture where a photograph should be.
        return _static_fallback(fallback, alt, css, priority, ratio, style)

    try:
        src = image.url
        name = image.name
    except Exception:
        return _static_fallback(fallback, alt, css, priority, ratio, style)

    row = lookup(name)
    sizes_attr = SIZES.get(sizes, sizes)

    src_attr = "data-src" if deferred else "src"
    attrs = [
        f'{src_attr}="{escape(src)}"',
        f'alt="{escape(alt or "")}"',
        'decoding="async"',
    ]
    if css:
        attrs.append(f'class="{escape(css)}"')

    if priority:
        attrs.append('fetchpriority="high"')
    elif not deferred:
        attrs.append(f'loading="{escape(loading)}"')

    inline = []
    if row:
        # Intrinsic dimensions reserve the space before the bytes arrive,
        # so nothing below the image jumps when it loads.
        attrs.append(f'width="{row.width}" height="{row.height}"')
        if row.focal_x != 50 or row.focal_y != 50:
            inline.append(f"object-position:{row.focal_x}% {row.focal_y}%")
    if ratio:
        inline.append(f"aspect-ratio:{ratio}")
    if style:
        inline.append(style.rstrip(";"))
    if inline:
        attrs.append(f'style="{escape(";".join(inline))}"')

    img = f"<img {' '.join(attrs)}>"

    if not row or not row.variants:
        return mark_safe(img)

    from django.core.files.storage import default_storage

    entries = []
    for width in sorted(row.variants, key=int):
        try:
            url = default_storage.url(row.variants[width])
        except Exception:
            continue
        entries.append(f"{escape(url)} {width}w")
    if not entries:
        return mark_safe(img)

    srcset_attr = "data-srcset" if deferred else "srcset"
    source = (
        f'<source type="image/webp" {srcset_attr}="{", ".join(entries)}" '
        f'sizes="{escape(sizes_attr)}">'
    )
    return mark_safe(f"<picture>{source}{img}</picture>")


@register.simple_tag
def focal_style(image):
    """Just the object-position for an image, for templates that cannot use
    the tag above — a CSS background, or an <img> inside third-party markup."""
    row = lookup(image.name) if image else None
    if not row:
        return ""
    return mark_safe(f"object-position:{row.focal_x}% {row.focal_y}%")


@register.simple_tag(takes_context=True)
def share_url(context, image=None):
    """An absolute url for a share card.

    The detail templates were building this as `{{ site_base_url }}{{
    image.url }}`, which is right on this machine and wrong in production:
    with Supabase storage `image.url` is already absolute, so the result
    was the site's own domain glued to the front of a supabase.co url.
    Falls back to the site-wide card when a page has no picture of its own.
    """
    request = context.get("request")
    if image:
        try:
            url = image.url
        except Exception:
            url = ""
        if url.startswith(("http://", "https://")):
            return url
        if url and request is not None:
            return request.build_absolute_uri(url)
    return context.get("share_image", "")
