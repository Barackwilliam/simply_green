"""Load the client's photo albums from the Google Photos links they shared.

The albums are listed in `apps/gallery/albums.json`: title, description and
the address of every photograph, read from the client's share links. The
pictures themselves are not in the repository. Six hundred photographs is
well over a hundred megabytes, and git keeps every byte of it forever. They
are fetched from Google at deploy time and saved through the normal storage,
so they land in the Supabase bucket like any upload.

Runs in the build because the free plan has no shell. It is idempotent: a
photograph already in storage is skipped, so after the first deploy this
takes seconds. It never fails the build. A picture it cannot fetch is
reported and left out, and the next deploy tries again.

Personal photographs that were in one of the shared albums were left out
of the manifest by hand. If the client adds pictures to an album later, the
manifest has to be regenerated; nothing here reads the live album list
except to refresh an address that has stopped working.

    python manage.py import_albums
    python manage.py import_albums --album kawe-beach-clean-up --limit 5
"""

import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import close_old_connections, connection

from apps.gallery.models import Album, Photo

MANIFEST = Path(__file__).resolve().parents[2] / "albums.json"

# Google resizes on its side. A gallery slide is at most 430 CSS pixels
# wide, so 1400 covers it on any screen with room to spare; the renditions
# then stop at 1100 instead of also making a 1600 nobody is shown. On the
# Supabase free plan's 1 GB this is the difference between the albums
# taking a quarter of the bucket and well over half of it.
SIZE = "=w1400-h1400"
JPEG_QUALITY = 80

# The cover is also the album page's banner, which runs the full width of
# the screen, so it is fetched at the size the optimiser keeps.
COVER_SIZE = "=w1800-h1800"

USER_AGENT = "Mozilla/5.0 (compatible; site-build)"
TIMEOUT = 60
WORKERS = 6


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def _compress(data):
    """Recompress Google's JPEG, which is generous, if that saves anything."""
    try:
        import io

        from PIL import Image

        image = Image.open(io.BytesIO(data))
        out = io.BytesIO()
        image.convert("RGB").save(
            out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
        )
        return out.getvalue() if out.tell() < len(data) else data
    except Exception:
        return data


def _token(photo_id):
    """The part of Google's id that goes in the filename.

    The filename is how a photograph is recognised on the next run: Photo
    has no field for an external id, and adding one for an import that runs
    a handful of times is not worth a migration. Storage may add a suffix
    and the optimiser may change the extension, but both keep the stem.
    """
    return re.sub(r"[^A-Za-z0-9_-]", "", photo_id)[-20:]


def _live_addresses(share_url):
    """Read the share page again for current photo addresses, by id."""
    html = _fetch(share_url).decode("utf-8", "replace")
    return dict(
        re.findall(
            r'\["(AF1Qip[A-Za-z0-9_-]+)",\["(https://lh3\.googleusercontent\.com/[^"]+)"',
            html,
        )
    )


class Command(BaseCommand):
    help = "Import the client's Google Photos albums into the gallery."

    def add_arguments(self, parser):
        parser.add_argument("--album", help="Only this album slug.")
        parser.add_argument(
            "--limit", type=int, default=0,
            help="At most this many photographs per album (for testing).",
        )

    def handle(self, *args, **options):
        try:
            self._run(options)
        except Exception as exc:  # never fail the build over photographs
            self.stdout.write(self.style.WARNING(f"  import_albums stopped: {exc}"))

    def _run(self, options):
        albums = json.loads(MANIFEST.read_text())["albums"]
        if options["album"]:
            albums = [a for a in albums if a["slug"] == options["album"]]

        for order, spec in enumerate(albums):
            album, _ = Album.objects.update_or_create(
                slug=spec["slug"],
                defaults=dict(
                    title=spec["title"],
                    description=spec["description"],
                    location=spec["location"],
                    date=date.fromisoformat(spec["date"]) if spec["date"] else None,
                    display_order=order,
                    is_featured=True,
                ),
            )
            photos = spec["photos"]
            if options["limit"]:
                photos = photos[: options["limit"]]
            added, failed = self._photos(album, spec, photos)
            self._cover(album, spec)
            self.stdout.write(
                f"  {album.slug}: {len(photos)} listed, {added} added"
                + (f", {failed} could not be fetched" if failed else "")
            )

    # -- photographs ------------------------------------------------------

    def _present(self, album):
        """Tokens of the photographs this album already has in storage."""
        have = set()
        for photo in album.photos.all():
            name = photo.image.name if photo.image else ""
            if not name:
                continue
            try:
                if not photo.image.storage.exists(name):
                    continue
            except Exception:
                pass
            have.add(name)
        return have

    def _photos(self, album, spec, photos):
        stored = self._present(album)
        todo = [
            (i, pid, url) for i, (pid, url) in enumerate(photos)
            if not any(_token(pid) in name for name in stored)
        ]
        if not todo:
            return 0, 0

        live = None
        failed = []

        def work(job):
            nonlocal live
            i, pid, url = job
            close_old_connections()
            try:
                try:
                    data = _fetch(url + SIZE)
                except Exception:
                    # Google's addresses for shared photographs can change.
                    # The share page has the current one.
                    if live is None:
                        live = _live_addresses(spec["share_url"])
                    if pid not in live:
                        raise
                    data = _fetch(live[pid] + SIZE)

                # A row left behind by a deploy whose disk was wiped is
                # given its picture back rather than duplicated.
                photo = album.photos.filter(image="").filter(display_order=i).first()
                if photo is None:
                    photo = Photo(album=album, display_order=i)
                photo.alt_text = spec["alt"]
                photo.image.save(
                    f"{album.slug}-{_token(pid)}.jpg",
                    ContentFile(_compress(data)),
                    save=True,
                )
                return True
            except Exception as exc:
                failed.append((pid, exc))
                return False
            finally:
                close_old_connections()

        # SQLite allows one writer at a time; in parallel, renditions fail
        # with "database is locked". Postgres has no such problem.
        workers = 1 if connection.vendor == "sqlite" else WORKERS
        with ThreadPoolExecutor(workers) as pool:
            added = sum(pool.map(work, todo))

        for pid, exc in failed[:5]:
            self.stdout.write(f"    could not fetch {pid}: {exc}")
        return added, len(failed)

    def _cover(self, album, spec):
        if album.cover_image:
            try:
                if album.cover_image.storage.exists(album.cover_image.name):
                    return
            except Exception:
                return
        url = next((u for pid, u in spec["photos"] if pid == spec["cover"]), None)
        try:
            data = _fetch(url + COVER_SIZE) if url else None
        except Exception:
            data = None
        if data is None:
            # Not reachable: the first photograph already stored will do.
            source = album.photos.exclude(image="").first()
            if source is None:
                return
            with source.image.open("rb") as handle:
                data = handle.read()
        album.cover_image.save(
            f"{album.slug}-cover.jpg", ContentFile(data), save=True
        )
