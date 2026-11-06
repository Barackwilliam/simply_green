"""Create the first admin account during deployment.

Render's free plan has no shell, so `createsuperuser` cannot be run by hand
after a deploy. This command runs as part of the build instead. It is
idempotent: it creates the account only when none with that username exists,
and never changes an existing one — so a password changed in the admin is
not silently reset on the next deploy.

Reads DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL and
DJANGO_SUPERUSER_PASSWORD. Does nothing, quietly, if they are not set.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError, ProgrammingError


class Command(BaseCommand):
    help = "Create the initial superuser from environment variables, if absent."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not (username and password):
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME/PASSWORD not set — skipping."
            )
            return

        User = get_user_model()

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.SUCCESS(f"Superuser '{username}' already exists.")
                )
                return

            User.objects.create_superuser(
                username=username, email=email or "", password=password
            )
        except (OperationalError, ProgrammingError) as exc:
            # The table may not exist yet on a very first, partial deploy.
            self.stderr.write(f"Could not create superuser: {exc}")
            return

        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
