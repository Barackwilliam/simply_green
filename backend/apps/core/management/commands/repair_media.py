"""Reconcile what the database says about images with what storage has.

On a host with no persistent disk the database outlives the uploads. A
redeploy leaves every ImageField holding a path to a file that is gone,
and the site renders a page of broken pictures — which is exactly what
happened in production.

The seed commands restore the images they put there in the first place.
This handles the rest: photographs an editor uploaded, which no command
can bring back. Those columns are cleared, so the templates fall back to
their placeholder instead of pointing at nothing. A missing picture is a
disappointment; a broken one looks like a broken site.

Rendition rows whose files are gone are rebuilt when the master is still
there and deleted when it is not — a rendition row is a promise that a
srcset can be written, and a srcset of 404s has no fallback, because a
<source> that fails is never retried against the <img>.

    python manage.py repair_media            # report and fix
    python manage.py repair_media --dry-run  # report only
"""

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import ImageField

from apps.core.renditions import ImageRendition, build


class Command(BaseCommand):
    help = "Clear image fields and renditions whose files are missing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change without changing it.",
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        cleared = rebuilt = dropped = checked = 0

        # --- image fields --------------------------------------------------
        for model in apps.get_models():
            fields = [
                f for f in model._meta.get_fields() if isinstance(f, ImageField)
            ]
            if not fields:
                continue
            for obj in model.objects.all().iterator():
                dirty = []
                for field in fields:
                    filefield = getattr(obj, field.name, None)
                    if not filefield or not filefield.name:
                        continue
                    checked += 1
                    try:
                        if filefield.storage.exists(filefield.name):
                            continue
                    except Exception:
                        continue
                    self.stdout.write(
                        f"  missing  {model._meta.label}.{field.name} "
                        f"#{obj.pk}: {filefield.name}"
                    )
                    if not dry:
                        setattr(obj, field.name, None)
                        dirty.append(field.name)
                    cleared += 1
                if dirty:
                    obj.save(update_fields=dirty)

        # --- renditions ----------------------------------------------------
        from django.core.files.storage import default_storage

        for row in ImageRendition.objects.all().iterator():
            present = False
            for path in row.variants.values():
                try:
                    present = default_storage.exists(path)
                except Exception:
                    present = True
                break
            if present:
                continue

            master_there = False
            try:
                master_there = default_storage.exists(row.source)
            except Exception:
                master_there = True

            if master_there:
                # The master survived, so the smaller copies can be made
                # again rather than the page falling back to the full-size
                # original on every screen.
                self.stdout.write(f"  rebuild  {row.source}")
                if not dry:
                    from django.core.files.storage import default_storage as st

                    class _Shim:
                        """build() wants something that behaves like a
                        FieldFile; the master's path and the storage are
                        all it actually uses."""

                        def __init__(self, name):
                            self.name = name
                            self.storage = st

                        def open(self, mode="rb"):
                            self._f = st.open(self.name, mode)
                            return self._f

                        def read(self):
                            return self._f.read()

                    build(_Shim(row.source), force=True)
                rebuilt += 1
            else:
                self.stdout.write(f"  drop     {row.source}")
                if not dry:
                    row.delete()
                dropped += 1

        self.stdout.write("")
        verb = "would be" if dry else "were"
        self.stdout.write(
            f"  {checked} image fields checked; {cleared} {verb} cleared, "
            f"{rebuilt} rendition sets rebuilt, {dropped} dropped."
        )
        if cleared and not dry:
            self.stdout.write(
                self.style.WARNING(
                    "\n  Those photographs are gone, not hidden. They were on a "
                    "disk that does not survive a deploy.\n  Set the Supabase "
                    "Storage keys so uploads go to the bucket instead:\n"
                    "  SUPABASE_PROJECT_REF, SUPABASE_S3_ACCESS_KEY_ID and\n"
                    "  SUPABASE_S3_SECRET_ACCESS_KEY, from Project Settings "
                    "-> Storage -> S3 access keys.\n"
                )
            )
