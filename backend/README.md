# Simply Green Organization — backend

Django 5 + Django REST Framework. Serves the JSON API the Next.js frontend
reads, and the admin panel the organisation's staff use to manage content.

## Stack

| Piece | Choice |
|---|---|
| Framework | Django 5.1 |
| API | Django REST Framework |
| Database | Supabase Postgres (Django ORM owns the schema) |
| File storage | Supabase Storage, via its S3-compatible API |
| Admin UI | [Unfold](https://unfoldadmin.com/) |
| Rich text | CKEditor 5 |
| Serving | Gunicorn + WhiteNoise |

## Running locally

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env        # then fill in the blanks
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/
API root: http://127.0.0.1:8000/api/

With `DATABASE_URL` left blank the project falls back to SQLite, so it boots
before any Supabase credentials exist.

## Apps

| App | Holds |
|---|---|
| `core` | Site settings, social links, partners/donors, impact statistics |
| `about` | Core values, objectives, "why partner with us", team members |
| `programmes` | Focus areas, programmes/projects, outcomes, programme images |
| `resources` | Publications: annual, financial, project reports, research |
| `news` | Posts (news, announcements, impact stories, podcasts), events, registrations |
| `gallery` | Photo albums, photos, videos |
| `engage` | Contact messages, volunteers, partner enquiries, newsletter, donations |

## API

All read endpoints are public and unauthenticated. Write endpoints accept
submissions only — the public cannot read back what others submitted.

```
GET  /api/site-settings/
GET  /api/partners/              ?kind=donor&is_featured=true
GET  /api/impact-stats/
GET  /api/about/core-values/
GET  /api/about/objectives/
GET  /api/about/partner-reasons/
GET  /api/about/team/            ?group=leadership
GET  /api/programmes/            ?status=ongoing&focus_areas__slug=climate-action
GET  /api/programmes/{slug}/
GET  /api/programmes/focus-areas/
GET  /api/resources/publications/   ?kind=annual_report&year=2025
GET  /api/news/posts/            ?kind=news&category__slug=climate
GET  /api/news/posts/{slug}/
GET  /api/news/events/           ?when=upcoming
GET  /api/gallery/albums/
GET  /api/gallery/videos/
GET  /api/engage/donation-methods/

POST /api/news/event-registrations/
POST /api/engage/contact/
POST /api/engage/volunteer/
POST /api/engage/partner-enquiry/
POST /api/engage/newsletter/
POST /api/engage/donate/
```

Submission endpoints are rate limited to 10 per hour per IP and carry a
honeypot field (`website_url`) that must be left empty.

## Health check

`GET /healthz/` returns `200` with `{"status": "ok", "database": true}` when
the database is reachable, `503` otherwise. Render uses this.

## A note on donation details

`DonationMethod` holds bank and mobile money details that are **published on
the website**, so they contain no secrets. They must still be verified with
the organisation's leadership directly — by phone or in person — before going
live. Substituted account numbers are a common fraud, and a donation page is
exactly where it pays off.

Payment *gateway* credentials (M-Pesa API keys, Selcom or DPO merchant
secrets) never belong in the database or in this repository. They go in
environment variables if and when a gateway is integrated.
