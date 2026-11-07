"""Is the bucket real, and can a browser read what we put in it?

Three things can be wrong and they look identical from the outside: the
variables are not all set, the keys are wrong, or the bucket is private.
Only the last one lets every upload succeed while every photograph stays
invisible, which is why "it uploaded fine" is not evidence of anything.

Shared by `manage.py checkmedia` and the admin dashboard. The dashboard
is the one that matters: the free plan has no shell, so a management
command is not somewhere the person who needs this answer can go.

Cached, because it writes a file to the bucket and reads it back over
the network, and the answer changes about twice in the life of a
project.
"""

import logging
import urllib.request
import uuid

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

CACHE_KEY = "storage-probe"
CACHE_TTL = 600
PAYLOAD = b"simply-green storage check"


def state():
    """Configuration only — no network. Always cheap."""
    missing = list(getattr(settings, "SUPABASE_STORAGE_MISSING", []))
    return {
        "active": bool(settings.USE_SUPABASE_STORAGE),
        "missing": missing,
        "debug": bool(settings.DEBUG),
        "backend": settings.STORAGES["default"]["BACKEND"].rsplit(".", 1)[-1],
        "media_url": settings.MEDIA_URL,
        "bucket": getattr(settings, "AWS_STORAGE_BUCKET_NAME", "") or "",
    }


def probe(force=False):
    """Write a file, read it back over http, delete it. Cached.

    Returns the configuration plus:
        wrote     — the bucket accepted an upload
        readable  — a plain http get of the public url returned it
        url       — that url, for showing in a message
        error     — what went wrong, if anything
    """
    base = state()
    if not base["active"]:
        return {**base, "wrote": False, "readable": False, "url": "", "error": ""}

    if not force:
        cached = cache.get(CACHE_KEY)
        if cached is not None:
            return cached

    result = {**base, "wrote": False, "readable": False, "url": "", "error": ""}
    name = f"healthcheck/{uuid.uuid4().hex}.txt"
    saved = None
    try:
        saved = default_storage.save(name, ContentFile(PAYLOAD))
        result["wrote"] = True
    except Exception as exc:
        result["error"] = f"{exc.__class__.__name__}: {exc}"
        cache.set(CACHE_KEY, result, CACHE_TTL)
        return result

    try:
        result["url"] = default_storage.url(saved)
    except Exception as exc:
        result["error"] = f"no public url: {exc}"

    if result["url"]:
        try:
            with urllib.request.urlopen(result["url"], timeout=20) as response:
                body = response.read(len(PAYLOAD) + 16)
            result["readable"] = response.status == 200 and body.startswith(PAYLOAD)
            if not result["readable"]:
                result["error"] = f"the url answered {response.status}"
        except Exception as exc:
            result["error"] = f"{exc.__class__.__name__}: {exc}"

    try:
        default_storage.delete(saved)
    except Exception as exc:  # pragma: no cover
        logger.warning("Could not delete the storage probe file: %s", exc)

    cache.set(CACHE_KEY, result, CACHE_TTL)
    return result
