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

from django.conf import settings
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
        # Same probe the admin dashboard runs, so the two can never give
        # different answers about the same bucket.
        from apps.core.storagecheck import probe

        self.stdout.write(self.style.MIGRATE_HEADING("\nWriting a test file\n"))
        result = probe(force=True)

        if not result["wrote"]:
            self.stdout.write(BAD + f"the bucket refused the upload: {result['error']}")
            self.stdout.write(
                self.style.ERROR(
                    "\n  The variables are set, so this is the keys or the "
                    "bucket.\n  Check a bucket named "
                    f"'{result['bucket']}' exists in this project and that\n"
                    "  the S3 keys belong to the same project.\n"
                )
            )
            return

        self.stdout.write(OK + "the bucket accepted it")
        if result["url"]:
            self.stdout.write(f"          {result['url']}")

        if result["readable"]:
            self.stdout.write(OK + "a browser can read it back")
            self.stdout.write(
                self.style.SUCCESS(
                    "\n  Uploads go to the bucket and will survive a deploy.\n"
                )
            )
            return

        self.stdout.write(BAD + f"a browser cannot read it: {result['error']}")
        self.stdout.write(
            self.style.ERROR(
                "\n  The upload worked, so the keys are right. The bucket is\n"
                "  private — which is how Supabase creates one. Open\n"
                f"  Storage -> {result['bucket']} and make it public, or the\n"
                "  site will write photographs it can never show.\n"
            )
        )
