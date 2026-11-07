# Simply Green Organization — website

The public website and content management system for **Simply Green
Organization (SGO)**, a Tanzanian NGO registered under the Non-Governmental
Organizations Act No. 24 of 2002 (Registration No. 00NGO/R5315), working on
environmental sustainability, climate action, community empowerment and
sustainable livelihoods across Mainland Tanzania.

## Architecture

One Django service renders the public site, serves the admin the
organisation's staff use, and exposes a JSON API for anything that needs it
later.

```
┌──────────────────────────────┐        ┌────────────────────────┐
│  Django 5                    │ ─────> │  Supabase              │
│  · public site (templates)   │        │  Postgres + Storage    │
│  · admin (Unfold)            │ <───── │                        │
│  · JSON API (DRF)            │        └────────────────────────┘
└──────────────────────────────┘
```

| Piece | Choice | Why |
|---|---|---|
| Framework | Django 5 | One service: no separate frontend to build, deploy or keep in step |
| Templates | Django + plain CSS | No build step, no Node, no bundler |
| Admin UI | [Unfold](https://unfoldadmin.com/) | A current interface rather than stock Django admin |
| Database | Supabase Postgres | Managed, with Django migrations as the source of truth |
| Files | Supabase Storage (S3 API) | Images and PDFs from a CDN, not the app server |
| Hosting | Render, Frankfurt | Same region as the database |

### Design

The structure follows the reference the client chose — a full-bleed hero,
three solid colour cards overlapping it, a full-width panel over a photo band,
bold uppercase navigation — using the organisation's own blue, green and gold.
Those hues are darkened wherever white text sits on them so every combination
clears WCAG AA, which the reference does not.

### A note on caching

The views deliberately do **not** use `cache_page`. The newsletter form sits
in the footer of every page, so every page carries a CSRF token, and a cached
page would serve the first visitor's token to everyone — which Django rejects
with a 403. This was found by testing the form, not by reading the code. If
caching is wanted later, cache the fragments that carry no token.

## Repository layout

```
backend/
  config/            settings, URL routing, health check
  apps/site/         public website: views, forms, navigation, sitemaps
  apps/core/         site settings, social links, partners, impact statistics
  apps/about/        core values, objectives, partner reasons, team
  apps/programmes/   focus areas, programmes, outcomes, images
  apps/resources/    publications and reports
  apps/news/         posts, events, event registrations
  apps/gallery/      albums, photos, videos
  apps/engage/       contact, volunteers, partners, newsletter, donations
  templates/         base, partials, one template per page
  static/            stylesheet, script, images
assets/source/       original photographs and logo supplied by the client
render.yaml          Render Blueprint — one service
```

## Running locally

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env            # then fill in the blanks
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_content      # loads the content draft
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Site: http://127.0.0.1:8000/ · Admin: http://127.0.0.1:8000/admin/

With `DATABASE_URL` blank the project falls back to SQLite, so it boots before
any Supabase credentials exist.

## Deploying

In Render choose **New → Blueprint** and point it at this repository. It
creates one service in Frankfurt and prompts for the secrets marked
`sync: false`:

| Secret | Where to find it |
|---|---|
| `DATABASE_URL` | Supabase → Project Settings → Database → Connection string → **Session pooler** |
| `SUPABASE_PROJECT_REF` | The project reference in the Supabase dashboard URL |
| `SUPABASE_S3_ACCESS_KEY_ID` / `SUPABASE_S3_SECRET_ACCESS_KEY` | Supabase → Project Settings → Storage → S3 access keys |
| `DJANGO_SUPERUSER_USERNAME` / `EMAIL` / `PASSWORD` | Your choice — this is how you first log in |
| `CSRF_TRUSTED_ORIGINS` | The site's own `https://` address |
| Email settings | Your SMTP provider |

Migrations, the first admin account and the content draft all run during the
build, because the free plan has no shell. All three steps are idempotent.

### When Postgres says "password authentication failed"

```bash
python manage.py checkdb
```

It pulls `DATABASE_URL` apart and says which of the three causes it is,
without printing the password. They produce the same message from Postgres
but need different fixes:

- **The username does not match the host.** The session pooler
  (`aws-0-<region>.pooler.supabase.com`) wants `postgres.<project-ref>`;
  only the direct host (`db.<ref>.supabase.co`) wants a plain `postgres`.
  Editing a username by hand after pasting a URI is how they get crossed.
- **The password contains a character a URL splits on** — usually `@`.
  Everything after it is read as part of the address, so the server is sent
  a fragment of the password and rejects it. Percent-encode it:
  ```bash
  python -c "import urllib.parse,getpass;print(urllib.parse.quote(getpass.getpass('password: '), safe=''))"
  ```
- **The password really is wrong.** Settle it without touching `.env`:

  ```bash
  python manage.py checkdb --ask
  ```

  It prompts for a password, encodes it correctly, and tries that. If it
  connects, the password is fine and `.env` was mangling it — the command
  prints the exact line to paste. If it is refused too, the password is
  wrong: it is **not** your Supabase account password, and it is shown only
  once when the project is created. Reset it under Project Settings →
  Database → Reset database password. Check also that the project is not
  paused; a free project sleeps after a week unused.

Two further traps the command also reports: port `6543` is the transaction
pooler and cannot run migrations, and `db.<ref>.supabase.co` is IPv6-only on
the free plan, so it will not connect at all from an IPv4-only network.

One more worth knowing: through the pooler, Postgres reports the failure
against user `postgres`, not the `postgres.<ref>` in your URL. That is
normal — the pooler reads the project reference, routes on it, then
authenticates upstream as `postgres`. It is not evidence of a username
problem.

None of this is needed to work on the site — leave `DATABASE_URL` blank and
Django uses a local SQLite file.

**`DATABASE_URL` is not optional in production.** Without it Django falls back
to SQLite on an ephemeral disk and every restart silently discards all
content. It warns loudly in the logs when this happens.

## A note on donation details

`DonationMethod` holds bank and mobile money details that are **published on
the website**, so they contain no secrets. They must still be verified with
the organisation's leadership directly — by phone or in person — before going
live. Substituting an account number is a common fraud, and a donation page is
exactly where it pays off.

Payment *gateway* credentials (M-Pesa API keys, Selcom or DPO merchant
secrets) never belong in this repository or the database.

The donation form records a donor's **intent to give**. It never asks for a
card number, PIN or mobile money password.

## Still needed from the organisation

- Contact details: phone, email, office address, social media links
- Real impact statistics — these must be theirs, not invented
- Team members: names, roles, photographs, short biographies
- Bank and mobile money details for donations
- Partner and donor logos
- Annual, financial and project reports
- The domain name
