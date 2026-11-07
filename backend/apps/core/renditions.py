"""Smaller, modern copies of every uploaded photograph.

A phone 390 pixels wide was downloading the same 1800-pixel JPEG as a
desktop — about ten times the pixels it can show, over the connection least
able to afford them. This module makes a WebP copy at each width the layout
actually asks for, once, when the image is saved, and records what it made.

Why a table rather than guessing the filenames: the template has to know
which widths exist before it writes a srcset, and a 404 inside a srcset is
a broken image, not a fallback. Asking the storage backend per image per
request would mean a round trip to Supabase on every card on every page.
One row, read through the cache, costs nothing.

Keyed by the master's storage path rather than by a foreign key, so it
serves every model with an ImageField without ten migrations, and two
models pointing at the same upload share the work.
"""

import io
import logging

from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models

logger = logging.getLogger(__name__)

# The widths the layout asks for, allowing for a 2x screen:
#   420  - a card or a hero on a phone
#   760  - a card on a tablet, a hero on a phone at 2x
#  1100  - a card at 2x, a hero on a tablet
#  1600  - a full-bleed hero on a desktop
WIDTHS = (420, 760, 1100, 1600)

WEBP_QUALITY = 78

CACHE_PREFIX = "rend:"
CACHE_TTL = 60 * 60 * 6


class ImageRendition(models.Model):
    """What was generated from one uploaded image, and how to frame it."""

    source = models.CharField(
        max_length=400,
        unique=True,
        db_index=True,
        help_text="Storage path of the uploaded image these belong to.",
    )
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    # {"420": "news/r/foo-420.webp", "760": ...}
    variants = models.JSONField(default=dict, blank=True)

    # Which point of the photograph to keep when a frame is a different
    # shape from the image. Percentages, as CSS object-position takes them.
    # 38% rather than 50% down: in a photograph of people standing, the
    # faces are above the middle, and the middle is where a wide frame cuts.
    focal_x = models.PositiveSmallIntegerField(
        default=50,
        verbose_name="Focus from the left",
        help_text="0 is the left edge, 100 the right. 50 is centred.",
    )
    focal_y = models.PositiveSmallIntegerField(
        default=38,
        verbose_name="Focus from the top",
        help_text="0 is the top edge, 100 the bottom. 38 keeps faces in "
                  "frame in most photographs of people standing.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Image rendition"

    def __str__(self):
        return f"{self.source} ({self.width}x{self.height})"

    @property
    def is_portrait(self):
        return bool(self.height) and self.width < self.height

    @property
    def aspect(self):
        return (self.width / self.height) if self.height else 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(CACHE_PREFIX + self.source)


def lookup(name):
    """The rendition row for a storage path, through the cache.

    Returns None when the image has not been through the pipeline — the
    template falls back to a plain <img> on the master file, which is
    always correct, just heavier.
    """
    if not name:
        return None
    key = CACHE_PREFIX + name
    cached = cache.get(key)
    if cached is not None:
        return cached or None
    row = ImageRendition.objects.filter(source=name).first()
    # Cache the miss too, as False — an image with no renditions is the
    # common case during the first seconds after a deploy, and it should
    # not mean a query per card per request.
    cache.set(key, row or False, CACHE_TTL)
    return row


PRESENT_PREFIX = "imgok:"
PRESENT_TTL = 600


def present(fieldfile):
    """Is the file behind this field actually in storage?

    The database is not evidence. On a host that rebuilds its disk every
    deploy and keeps the database, every ImageField goes on holding a
    path to a file that is gone, and the page renders a broken picture
    where a photograph should be.

    One storage call per image per ten minutes, cached: a stat on local
    disk, a HEAD against the bucket. That is affordable, and the
    alternative — trusting the column — is what put a site full of
    broken images in front of the client twice.
    """
    try:
        name = fieldfile.name
    except Exception:
        return False
    if not name:
        return False

    key = PRESENT_PREFIX + name
    cached = cache.get(key)
    if cached is not None:
        return cached

    try:
        ok = fieldfile.storage.exists(name)
    except Exception:
        # If the backend cannot answer, assume the file is there: a
        # transient error should not blank every photograph on the site.
        ok = True
    cache.set(key, ok, PRESENT_TTL)
    return ok


def _variants_present(row):
    """True when the files this row names are actually in storage.

    A row is a claim about files, and on a host with no persistent disk
    the row outlives them. Trusting the claim meant writing a srcset of
    404s into the page: the browser then has no fallback, because a
    <source> that fails is not retried against the <img>.

    Checks one file, not all of them. They are written in a single pass,
    so either the set is there or it is not, and one call is enough to
    tell which.
    """
    for path in row.variants.values():
        try:
            return default_storage.exists(path)
        except Exception:
            return True
    return False


def build(fieldfile, *, force=False):
    """Make the WebP copies for one image and record them.

    Safe to call repeatedly: it returns the existing row untouched unless
    the master has changed shape or `force` is set.
    """
    try:
        from PIL import Image, ImageOps
    except ImportError:  # pragma: no cover
        return None

    name = fieldfile.name
    if not name:
        return None

    row = ImageRendition.objects.filter(source=name).first()
    if row and row.variants and not force and _variants_present(row):
        return row

    try:
        fieldfile.open()
        raw = fieldfile.read()
        image = Image.open(io.BytesIO(raw))
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
    except Exception as exc:
        logger.warning("Cannot build renditions for %s: %s", name, exc)
        return None

    master_w, master_h = image.size
    stem = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    folder = name.rsplit("/", 1)[0] if "/" in name else ""
    prefix = f"{folder}/r/" if folder else "r/"

    variants = {}
    for target in WIDTHS:
        # Never upscale: a 900px master gets 420 and 760, and stops.
        if target > master_w:
            continue
        copy = image.copy()
        copy.thumbnail((target, target * 4), Image.LANCZOS)
        buffer = io.BytesIO()
        copy.save(buffer, "WEBP", quality=WEBP_QUALITY, method=5)
        path = f"{prefix}{stem}-{target}.webp"
        if default_storage.exists(path):
            default_storage.delete(path)
        saved = default_storage.save(path, ContentFile(buffer.getvalue()))
        variants[str(target)] = saved

    # The master is always offered at its own width, so a very small upload
    # still has something in the srcset.
    if not variants:
        return None

    row, _ = ImageRendition.objects.update_or_create(
        source=name,
        defaults=dict(width=master_w, height=master_h, variants=variants),
    )
    logger.info(
        "Renditions for %s: %s widths from %sx%s",
        name, len(variants), master_w, master_h,
    )
    return row
