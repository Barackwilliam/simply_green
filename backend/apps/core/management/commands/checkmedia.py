"""Say whether uploaded photographs are being stored somewhere permanent.

Uploads go to the server's own disk unless three environment variables
are all set. Render rebuilds that disk on every deploy and keeps the
database, so the result is a site full of broken pictures — and the only
warning was a RuntimeWarning in a build log.

This names the variable that is actually missing, and when the
configuration looks complete it proves it by writing a small file to the
bucket, reading it back and deleting it. A key that is present but wrong
produces the same silence as no key at all, so "it looks configured" is
not worth reporting on its own.

    python manage.py checkmedia
"""

import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

OK = "  \033[32mok\033[0m    "
BAD = "  \033[31mX\033[0m     "
WARN = "  \033[33m!\033[0m     "

WHERE = (
    "Supabase dashboard -> Project Settings -> Storage -> S3 access keys\n"
    "       gives the access key id and the secret. The project reference\n"
    "       is the string in your project's own url:\n"
    "       https://supabase.com/dashboard/project/<THIS-BIT>"
)


class Command(BaseCommand):
    help = "Check that uploads are stored somewhere that survives a deploy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-write",
            action="store_true",
            help="Report the configuration without writing a test file.",
        )

    def handle(self, *args, **options):
        missing = list(getattr(settings, "SUPABASE_STORAGE_MISSING", []))
        active = settings.USE_SUPABASE_STORAGE
        backend = settings.STORAGES["default"]["BACKEND"].rsplit(".", 1)[-1]

        self.stdout.write(self.style.MIGRATE_HEADING("\nWhere uploads go\n"))
        self.stdout.write(f"  backend    {backend}")
        self.stdout.write(f"  MEDIA_URL  {settings.MEDIA_URL}")
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "") or getattr(
            settings, "SUPABASE_STORAGE_BUCKET", ""
        )
        self.stdout.write(f"  bucket     {bucket or '—'}")

        self.stdout.write(self.style.MIGRATE_HEADING("\nChecks\n"))

        if active:
            self.stdout.write(OK + "Supabase Storage is switched on")
        elif missing:
            self.stdout.write(
                BAD + "falling back to the server's own disk, because "
                + ("this is" if len(missing) == 1 else "these are")
                + " not set:"
            )
            for name in missing:
                self.stdout.write(f"          {name}")
            self.stdout.write("\n       " + WHERE)
            self.stdout.write(
                "\n       All three are needed. Two of them are called keys\n"
                "       and the third is not, which is how a configuration\n"
                "       that looks finished ends up half done.\n"
            )
        else:
            self.stdout.write(
                WARN + "all three variables are set, but USE_SUPABASE_STORAGE\n"
                "       is off. Set it to True."
            )

        if settings.DEBUG:
            self.stdout.write(
                WARN + "DEBUG is on, so this is a development machine and\n"
                "       the local disk is the right place anyway."
            )
            return

        if not active:
            self.stdout.write(
                self.style.ERROR(
                    "\n  Every photograph on this site will disappear on the\n"
                    "  next deploy, including any added through the admin.\n"
                )
            )
            return

        if options["no_write"]:
            return

        # --- prove it --------------------------------------------------
        self.stdout.write(self.style.MIGRATE_HEADING("\nWriting a test file\n"))
        name = f"healthcheck/{uuid.uuid4().hex}.txt"
        payload = b"simply-green storage check"
        try:
            saved = default_storage.save(name, ContentFile(payload))
            self.stdout.write(OK + f"wrote {saved}")
        except Exception as exc:
            self.stdout.write(BAD + f"could not write: {exc.__class__.__name__}: {exc}")
            self.stdout.write(
                self.style.ERROR(
                    "\n  The variables are set but the bucket refused the "
                    "upload.\n  Check the bucket named above exists and that "
                    "the keys belong\n  to this project.\n"
                )
            )
            return

        try:
            with default_storage.open(saved) as handle:
                back = handle.read()
            if back == payload:
                self.stdout.write(OK + "read it back unchanged")
            else:
                self.stdout.write(BAD + "read it back but the contents differ")
        except Exception as exc:
            self.stdout.write(BAD + f"could not read it back: {exc}")

        # Uploading proves the keys. It does not prove a browser can read
        # the file back: a Supabase bucket is private when it is created,
        # and a private bucket answers the public url with an error while
        # every write keeps succeeding.
        try:
            public = default_storage.url(saved)
        except Exception as exc:
            public = ""
            self.stdout.write(WARN + f"no public url: {exc}")

        if public:
            self.stdout.write(f"          {public}")
            try:
                import urllib.request

                with urllib.request.urlopen(public, timeout=20) as response:
                    code = response.status
                    body = response.read(len(payload) + 16)
                if code == 200 and body.startswith(payload):
                    self.stdout.write(OK + "a browser can read it back")
                elif code == 200:
                    self.stdout.write(
                        WARN + "the url answers 200 but with something else"
                    )
                else:
                    self.stdout.write(BAD + f"the url answers {code}")
            except Exception as exc:
                self.stdout.write(BAD + f"a browser cannot read it: {exc}")
                self.stdout.write(
                    "\n       The upload worked, so the keys are right. The\n"
                    "       bucket is private — which is how Supabase creates\n"
                    "       one. Open Storage -> the bucket -> settings and\n"
                    "       make it public, or the site can write photographs\n"
                    "       it can never show.\n"
                )

        try:
            default_storage.delete(saved)
            self.stdout.write(OK + "deleted the test file")
        except Exception as exc:
            self.stdout.write(WARN + f"left the test file behind: {exc}")

        self.stdout.write(
            self.style.SUCCESS(
                "\n  Uploads are going to the bucket and will survive a "
                "deploy.\n"
            )
        )
