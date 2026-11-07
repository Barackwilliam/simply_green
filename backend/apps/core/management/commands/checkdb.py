"""Explain what DATABASE_URL actually says, and why the connection fails.

"password authentication failed for user postgres" is the same message
whether the password is wrong, the username is wrong for the host, or the
password was silently cut in half by a character the url parser treats as
a delimiter. Those need different fixes, so this pulls the url apart and
says which it is, without ever printing the password.

    python manage.py checkdb
"""

import getpass
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

# Characters that end a field in a url. Unencoded in a password, the parser
# stops there and sends whatever came before, which the server then
# rejects as the wrong password.
BREAKS = "@/?#[]: "

OK = "  \033[32mok\033[0m   "
BAD = "  \033[31mX\033[0m    "
WARN = "  \033[33m!\033[0m    "


class Command(BaseCommand):
    help = "Check DATABASE_URL and report why Postgres is refusing it."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-connect",
            action="store_true",
            help="Only inspect the url; do not try to open a connection.",
        )
        parser.add_argument(
            "--ask",
            action="store_true",
            help=(
                "Ignore the password in .env, prompt for one, and try that "
                "instead. Settles whether the password is wrong or .env is "
                "mangling it."
            ),
        )

    def _connect(self, url):
        """Open one connection outside Django's configured alias."""
        import dj_database_url
        from django.db.utils import ConnectionHandler

        # ConnectionHandler insists on a "default" alias, and the ssl
        # requirement has to match the project's own setting or a local
        # Postgres with no TLS is refused for the wrong reason.
        config = dj_database_url.parse(
            url, ssl_require=getattr(settings, "DATABASE_SSL_REQUIRE", True)
        )
        handler = ConnectionHandler({"default": config})
        try:
            with handler["default"].cursor() as cursor:
                cursor.execute("select 1")
            return True
        except Exception as exc:
            self.stdout.write(BAD + f"{exc.__class__.__name__}: {exc}".strip())
            return False
        finally:
            try:
                handler.close_all()
            except Exception:
                pass

    def handle(self, *args, **options):
        raw = (getattr(settings, "DATABASE_URL", "") or "").strip()

        if not raw:
            self.stdout.write(
                "DATABASE_URL is empty, so Django is using the local SQLite "
                "file at backend/db.sqlite3.\n"
                "That is a perfectly good way to work on the site — you only "
                "need Supabase when you want the real content."
            )
            return

        parts = urlsplit(raw)
        user = unquote(parts.username or "")
        password = unquote(parts.password or "")
        host = parts.hostname or ""
        port = parts.port
        dbname = (parts.path or "").lstrip("/")

        self.stdout.write(self.style.MIGRATE_HEADING("\nWhat the url says\n"))
        self.stdout.write(f"  host      {host}")
        self.stdout.write(f"  port      {port}")
        self.stdout.write(f"  user      {user}")
        self.stdout.write(f"  database  {dbname}")
        raw_password = parts.password or ""
        self.stdout.write(f"  password  {len(password)} characters")
        if raw_password != password:
            self.stdout.write(
                "            (percent-decoded on the way through — if the "
                "real\n             password contains a literal %, it must "
                "be written %25)"
            )

        pooled = "pooler.supabase.com" in host
        direct = host.startswith("db.") and host.endswith(".supabase.co")

        self.stdout.write(self.style.MIGRATE_HEADING("\nChecks\n"))
        problems = []

        # --- the usual cause --------------------------------------------
        if pooled and "." not in user:
            problems.append(
                "The pooler needs the project reference in the username.\n"
                "       It wants  postgres.<project-ref>\n"
                f"       it has    {user}\n"
                "       Copy the whole URI from Supabase rather than editing\n"
                "       the username by hand: Project Settings -> Database\n"
                "       -> Connection string -> Session pooler."
            )
            self.stdout.write(BAD + "username does not match a pooler host")
        elif pooled:
            self.stdout.write(OK + f"username has a project reference ({user})")
        elif direct and "." in user:
            problems.append(
                "The direct host wants the plain username 'postgres'.\n"
                f"       It has {user}, which belongs to the pooler."
            )
            self.stdout.write(BAD + "pooler username on a direct host")
        elif direct:
            self.stdout.write(OK + "direct connection, plain username")
            self.stdout.write(
                WARN + "db.<ref>.supabase.co is IPv6-only on the free plan.\n"
                "       If your network has no IPv6 this will not connect at\n"
                "       all; use the session pooler instead."
            )
        else:
            self.stdout.write(WARN + "host is not a recognised Supabase host")

        # --- the second usual cause --------------------------------------
        # Checked against the raw string, not the parsed password: an
        # unencoded "@" splits the url at the wrong place, so by the time
        # urlsplit has finished, the password it reports is already a
        # harmless-looking fragment and the real evidence is the mangled
        # host beside it.
        after_scheme = raw.split("://", 1)[-1]
        creds = after_scheme.rsplit("@", 1)[0] if "@" in after_scheme else ""
        extra_at = creds.count("@")
        host_looks_wrong = bool(host) and "." not in host

        if extra_at or host_looks_wrong:
            problems.append(
                "The password contains a character a url splits on — almost\n"
                "       certainly '@'. Everything after it has been read as\n"
                f"       part of the address, which is why the host came out\n"
                f"       as '{host}'. Percent-encode the password; see below."
            )
            self.stdout.write(BAD + "the password has broken the url apart")
        else:
            # Only a flaw when the password was written raw. If decoding
            # changed it, these characters are already escaped and the url
            # is correct — flagging that was a false alarm on a working
            # connection.
            hit = [] if raw_password != password else [
                c for c in BREAKS if c in password
            ]
            if hit:
                shown = " ".join(repr(c) for c in hit)
                problems.append(
                    f"The password contains {shown}, which a url treats as a\n"
                    "       delimiter. It must be percent-encoded, or the server\n"
                    "       receives only the part before it. See below."
                )
                self.stdout.write(BAD + "password contains characters a url splits on")
            elif raw_password != password:
                self.stdout.write(OK + "password is percent-encoded")
            else:
                self.stdout.write(OK + "password needs no escaping")

        if password != password.strip():
            problems.append(
                "The password has a space or a line break at one end.\n"
                "       Check for a trailing space after the url in .env, or\n"
                "       a line that wrapped when it was pasted."
            )
            self.stdout.write(BAD + "password has whitespace at one end")

        if "YOUR-PASSWORD" in raw.upper() or "[" in (raw_password or ""):
            problems.append(
                "The url still contains Supabase's placeholder. The page\n"
                "       shows [YOUR-PASSWORD] where the real one goes; it is\n"
                "       not filled in for you."
            )
            self.stdout.write(BAD + "placeholder left in the url")

        if port == 6543:
            self.stdout.write(
                WARN + "port 6543 is the transaction pooler. It cannot run\n"
                "       migrations (no prepared statements). Use 5432."
            )
        elif port == 5432:
            self.stdout.write(OK + "port 5432")

        if not dbname:
            problems.append("No database name after the host. It should be /postgres.")
            self.stdout.write(BAD + "no database name")

        # --- try a password typed in, bypassing .env entirely -------------
        # The one test that separates "the password is wrong" from ".env is
        # mangling a password that is right". Typed in, encoded here, and
        # never written anywhere.
        if options["ask"]:
            self.stdout.write(self.style.MIGRATE_HEADING("\nTrying a typed password\n"))
            typed = getpass.getpass("  Database password (hidden): ")
            if not typed:
                self.stdout.write(BAD + "nothing entered")
                return
            if typed != typed.strip():
                self.stdout.write(
                    WARN + "what you typed has a space at one end; "
                    "trying it as typed"
                )
            netloc = (
                f"{quote(user, safe='')}:{quote(typed, safe='')}"
                f"@{host}{f':{port}' if port else ''}"
            )
            probe = urlunsplit((parts.scheme, netloc, parts.path, "", ""))
            if self._connect(probe):
                self.stdout.write(self.style.SUCCESS(
                    "\n  That password works.\n\n"
                    "  So the password is right and .env is the problem. Put\n"
                    "  this exact line in backend/.env, on one line, with no\n"
                    "  quotes around it and no space before or after the =:\n"
                ))
                masked = probe.replace(quote(typed, safe=""), "<password>")
                self.stdout.write(f"    DATABASE_URL={masked}\n")
                self.stdout.write(
                    "  with <password> replaced by the percent-encoded form:\n"
                    f"    {quote(typed, safe='')}\n"
                )
            else:
                self.stdout.write(self.style.ERROR(
                    "\n  That password is refused too, so it is not .env.\n\n"
                    "  The database password is not your Supabase account\n"
                    "  password, and it is only shown once when the project is\n"
                    "  created. Reset it: Project Settings -> Database ->\n"
                    "  Database password -> Reset database password.\n\n"
                    "  Check too that the project is not paused — a free\n"
                    "  project sleeps after a week unused, and the dashboard\n"
                    "  shows a Restore button when it has.\n"
                ))
            return

        # --- try it ------------------------------------------------------
        if not options["no_connect"]:
            self.stdout.write(self.style.MIGRATE_HEADING("\nConnecting\n"))
            try:
                with connections["default"].cursor() as cursor:
                    cursor.execute("select version()")
                    version = cursor.fetchone()[0]
                self.stdout.write(OK + version.split(",")[0])
                self.stdout.write(self.style.SUCCESS("\nThe connection works.\n"))
                return
            except Exception as exc:
                text = f"{exc}".strip()
                self.stdout.write(BAD + f"{exc.__class__.__name__}: {text}")
                if pooled and 'user "postgres"' in text:
                    self.stdout.write(
                        "\n" + WARN + "The server says user \"postgres\", not the\n"
                        "       name in the url. That is normal through the\n"
                        "       pooler — it reads the project reference, routes\n"
                        "       on it, then authenticates upstream as postgres.\n"
                        "       So this is not a username problem: the password\n"
                        "       is being rejected."
                    )

        if problems:
            self.stdout.write(self.style.MIGRATE_HEADING("\nWhat to fix\n"))
            for i, problem in enumerate(problems, 1):
                self.stdout.write(f"  {i}. {problem}\n")
            self.stdout.write(
                "  To percent-encode a password safely, run:\n\n"
                '    python -c "import urllib.parse,getpass;'
                "print(urllib.parse.quote(getpass.getpass('password: '), safe=''))\"\n\n"
                "  and paste the result into the url in place of the password.\n"
            )
        else:
            self.stdout.write(
                "\n  The url is well formed, so the password itself is being\n"
                "  rejected. Reset it in Supabase: Project Settings ->\n"
                "  Database -> Reset database password, then copy the whole\n"
                "  connection string again.\n"
            )

        self.stdout.write(
            "\n  You do not need any of this to work on the site. Leave\n"
            "  DATABASE_URL blank in backend/.env and Django uses a local\n"
            "  SQLite file instead.\n"
        )
