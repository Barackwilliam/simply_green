# Simply Green Organization — website

The public website and content management system for **Simply Green
Organization (SGO)**, a Tanzanian NGO registered under the Non-Governmental
Organizations Act No. 24 of 2002 (Registration No. 00NGO/R5315), working on
environmental sustainability, climate action, community empowerment and
sustainable livelihoods across Mainland Tanzania.

## Architecture

```
┌──────────────────┐        JSON API         ┌────────────────────┐
│  Next.js 16      │ ──────────────────────> │  Django 5 + DRF    │
│  (public site)   │                         │  (API + admin)     │
│                  │ <────────────────────── │                    │
└──────────────────┘   cache invalidation    └────────────────────┘
                                                       │
                                                       ▼
                                           ┌────────────────────────┐
                                           │  Supabase              │
                                           │  Postgres + Storage    │
                                           └────────────────────────┘
```

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 16, React 19, Tailwind v4 | Pages prerender to static HTML, which is what makes the site fast and indexable |
| Backend | Django 5 + DRF | Staff manage everything through one admin; the ORM owns the schema |
| Admin UI | [Unfold](https://unfoldadmin.com/) | A current interface rather than stock Django admin |
| Database | Supabase Postgres | Managed, with Django migrations as the source of truth |
| Files | Supabase Storage (S3 API) | Images and PDFs served from a CDN, not from the app server |
| Hosting | Render, Frankfurt | Same region as the database, so queries stay fast |

### How content reaches the site

The site is statically prerendered, so a page would normally keep serving the
previous version until its cache lapsed. Instead:

1. An editor saves something in the Django admin.
2. A `post_save` signal posts the affected cache tags to the frontend's
   `/api/revalidate` endpoint.
3. Next.js drops exactly those cache entries; the next request re-renders.

Measured end to end at roughly **four seconds**. The endpoint requires a
shared secret and refuses every request when that secret is unset, rather
than defaulting to open.

## Repository layout

```
backend/            Django project
  config/             settings, URL routing, health check
  apps/core/          site settings, social links, partners, impact stats
  apps/about/         core values, objectives, partner reasons, team
  apps/programmes/    focus areas, programmes, outcomes, images
  apps/resources/     publications and reports
  apps/news/          posts, events, event registrations
  apps/gallery/       albums, photos, videos
  apps/engage/        contact, volunteers, partners, newsletter, donations
frontend/           Next.js app
  app/                routes, sitemap, robots, revalidate endpoint
  components/         layout, UI primitives, cards, forms, home sections
  lib/                API client, types, utilities, navigation
assets/source/      Original photographs and logo supplied by the client
render.yaml         Render Blueprint for both services
```

## Running locally

Two terminals.

**Backend**

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # fill in the blanks
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_content     # loads the content draft
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env.local    # fill in the blanks
npm run dev
```

Site: http://localhost:3000 · Admin: http://127.0.0.1:8000/admin/

With `DATABASE_URL` left blank the backend falls back to SQLite, so it boots
before any Supabase credentials exist.

## Deploying

The repository ships a Render Blueprint. In Render, choose **New → Blueprint**
and point it at this repository. It creates two services in Frankfurt and
prompts for the secrets marked `sync: false`:

| Secret | Where to find it |
|---|---|
| `DATABASE_URL` | Supabase → Project Settings → Database → Connection string → **Session pooler** |
| `SUPABASE_PROJECT_REF` | The project reference in your Supabase dashboard URL |
| `SUPABASE_S3_ACCESS_KEY_ID` / `SUPABASE_S3_SECRET_ACCESS_KEY` | Supabase → Project Settings → Storage → S3 access keys |
| `REVALIDATE_SECRET` | Any long random string — **the same value on both services** |
| `NEXT_PUBLIC_SITE_URL` | The site's real public address |
| Email settings | Your SMTP provider |

Migrations run as part of the backend build, so the Supabase schema is created
on first deploy.

### After the first deploy

1. Create a superuser: Render → `simply-green-api` → Shell →
   `python manage.py createsuperuser`
2. Run `python manage.py seed_content` to load the content draft.
3. Fill in Site settings: contact details, social links, logo.
4. Add the real impact statistics, team members, partners and donation details.

## A note on donation details

`DonationMethod` holds bank and mobile money details that are **published on
the website**, so they hold no secrets. They must still be verified with the
organisation's leadership directly — by phone or in person — before going
live. Substituting an account number is a common fraud, and a donation page is
exactly where it pays off.

Payment *gateway* credentials (M-Pesa API keys, Selcom or DPO merchant
secrets) never belong in this repository or the database. They go in
environment variables if and when a gateway is integrated.

The donation form records a donor's **intent to give**. It never asks for a
card number, PIN or mobile money password.

## Still to come from the organisation

- Contact details: phone, email, office address, social media links
- Real impact statistics — these must be theirs, not invented
- Team members: names, roles, photographs, short biographies
- Bank and mobile money details for donations
- Partner and donor logos
- Annual, financial and project reports
- The domain name
