"""Downsize images as they are saved.

Photographs come off a phone at several thousand pixels and six megabytes.
Serving those untouched is the single heaviest thing a site like this can do,
and no editor should have to remember to resize before uploading — so it
happens here, once, on the way in.

Registered as a `pre_save` signal for every model that has an ImageField, so
new models get it without being wired up.
"""

import io
import logging

from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save

logger = logging.getLogger(__name__)

# Long edge in pixels. Comfortably above any slot on the site, including a
# full-bleed hero on a high-density screen, with nothing left over.
MAX_EDGE = 1800

# Below this there is nothing worth doing.
SKIP_UNDER_BYTES = 120 * 1024

JPEG_QUALITY = 82


def optimise(fieldfile) -> bool:
    """Shrink and recompress one image in place. True if it was rewritten."""
    try:
        from PIL import Image, ImageOps
    except ImportError:  # pragma: no cover
        return False

    try:
        fieldfile.open()
        raw = fieldfile.read()
    except Exception as exc:
        logger.warning("Could not read %s: %s", fieldfile.name, exc)
        return False

    if len(raw) < SKIP_UNDER_BYTES:
        return False

    try:
        image = Image.open(io.BytesIO(raw))
        image = ImageOps.exif_transpose(image)
    except Exception as exc:
        logger.warning("Not a readable image, left alone: %s (%s)", fieldfile.name, exc)
        return False

    has_alpha = image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )

    if max(image.size) > MAX_EDGE:
        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)

    buffer = io.BytesIO()
    if has_alpha:
        image.convert("RGBA").save(buffer, "PNG", optimize=True)
        suffix = ".png"
    else:
        image.convert("RGB").save(
            buffer, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
        )
        suffix = ".jpg"

    if buffer.tell() >= len(raw):
        # Already smaller than anything we would produce.
        return False

    stem = fieldfile.name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    fieldfile.save(f"{stem}{suffix}", ContentFile(buffer.getvalue()), save=False)
    logger.info(
        "Optimised %s: %.0f KB -> %.0f KB", fieldfile.name, len(raw) / 1024,
        buffer.tell() / 1024,
    )
    return True


def _handler(sender, instance, **kwargs):
    for field in sender._meta.get_fields():
        if not isinstance(field, ImageField):
            continue
        fieldfile = getattr(instance, field.name, None)
        if not fieldfile:
            continue
        # Only touch a file that has just been uploaded, never one already
        # stored — re-saving a model should not recompress its images again
        # and again, losing a little quality each time.
        if not hasattr(fieldfile.file, "content_type") and fieldfile._committed:
            continue
        try:
            optimise(fieldfile)
        except Exception as exc:
            logger.warning("Image optimisation failed for %s: %s", field.name, exc)


def register():
    """Connect the handler to every model that stores an image."""
    from django.apps import apps

    for model in apps.get_models():
        if any(isinstance(f, ImageField) for f in model._meta.get_fields()):
            pre_save.connect(
                _handler,
                sender=model,
                weak=False,
                dispatch_uid=f"optimise-images-{model._meta.label_lower}",
            )
