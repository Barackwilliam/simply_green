"""
Django settings for the Simply Green Organization website.

Configuration is environment-driven so the same code runs locally, on Render,
and in CI without edits. See `.env.example` for every variable this file reads.
"""

import warnings
from pathlib import Path

import dj_database_url
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
    USE_SUPABASE_STORAGE=(bool, False),
)

# Read .env when present. Never commit it — commit `.env.example` instead.
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-only-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

SITE_NAME = "Simply Green Organization"
SITE_SHORT_NAME = "SGO"

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    # Modern admin UI — must precede django.contrib.admin.
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third party
    "rest_framework",
    "django_filters",
    "taggit",
    "django_ckeditor_5",
    "ordered_model",
    "django_extensions",
    # Project apps
    "apps.core",
    "apps.site",
    "apps.about",
    "apps.programmes",
    "apps.resources",
    "apps.news",
    "apps.gallery",
    "apps.engage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.site.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Database — Supabase Postgres in every deployed environment.
# ---------------------------------------------------------------------------

DATABASE_URL = env("DATABASE_URL", default="")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=env.bool("DATABASE_SSL_REQUIRE", default=True),
        )
    }
else:
    # Local fallback so the project boots before Supabase credentials exist.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    if not DEBUG:
        # On a deployed host this is a trap, not a convenience: the container
        # has no persistent disk, so every restart silently discards all
        # content. Say so loudly rather than let it look like it works.
        warnings.warn(
            "DATABASE_URL is not set. Falling back to SQLite on an ephemeral "
            "disk — ALL DATA WILL BE LOST on the next restart or deploy. Set "
            "DATABASE_URL to the Supabase session-pooler connection string.",
            RuntimeWarning,
            stacklevel=2,
        )

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation — the site is published in English.
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media
#
# Static files are served by WhiteNoise. Media (editor uploads) go to the
# Supabase Storage bucket through its S3-compatible API once configured.
# ---------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

USE_SUPABASE_STORAGE = env("USE_SUPABASE_STORAGE")

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "apps.core.storage.ForgivingManifestStaticFilesStorage"
    },
}

SUPABASE_PROJECT_REF = env("SUPABASE_PROJECT_REF", default="")
SUPABASE_S3_ACCESS_KEY_ID = env("SUPABASE_S3_ACCESS_KEY_ID", default="")
SUPABASE_S3_SECRET_ACCESS_KEY = env("SUPABASE_S3_SECRET_ACCESS_KEY", default="")

# Storage is only switched over when the credentials to reach it are actually
# present. A half-configured bucket would otherwise take the whole site down
# at boot, which is a worse failure than serving uploads from local disk.
if USE_SUPABASE_STORAGE and not (
    SUPABASE_PROJECT_REF
    and SUPABASE_S3_ACCESS_KEY_ID
    and SUPABASE_S3_SECRET_ACCESS_KEY
):
    warnings.warn(
        "USE_SUPABASE_STORAGE is on but SUPABASE_PROJECT_REF and the S3 keys "
        "are not all set. Falling back to local file storage — uploads will "
        "not survive a restart. Add the S3 access keys from Supabase "
        "Project Settings -> Storage.",
        RuntimeWarning,
        stacklevel=2,
    )
    USE_SUPABASE_STORAGE = False

if USE_SUPABASE_STORAGE:
    SUPABASE_STORAGE_BUCKET = env("SUPABASE_STORAGE_BUCKET", default="media")
    SUPABASE_S3_REGION = env("SUPABASE_S3_REGION", default="eu-central-1")

    AWS_ACCESS_KEY_ID = SUPABASE_S3_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = SUPABASE_S3_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = SUPABASE_STORAGE_BUCKET
    AWS_S3_REGION_NAME = SUPABASE_S3_REGION
    AWS_S3_ENDPOINT_URL = (
        f"https://{SUPABASE_PROJECT_REF}.storage.supabase.co/storage/v1/s3"
    )
    # Supabase Storage requires path-style addressing.
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=31536000, immutable"}

    STORAGES["default"] = {"BACKEND": "storages.backends.s3.S3Storage"}

    MEDIA_URL = (
        f"https://{SUPABASE_PROJECT_REF}.supabase.co"
        f"/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/"
    )

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "120/min"},
}

# ---------------------------------------------------------------------------
# Trusted origins
# ---------------------------------------------------------------------------

def _as_origin(value: str) -> str:
    """Normalise a value into an origin Django accepts.

    CSRF_TRUSTED_ORIGINS requires a scheme: a bare hostname raises 4_0.E001 at
    startup, which fails the deploy. Hosting platforms and hand-typed settings
    routinely supply the host alone, so add https:// when it is missing rather
    than refuse to boot over a missing prefix.
    """
    value = value.strip().rstrip("/")
    if not value:
        return ""
    if "://" in value:
        return value
    return f"https://{value}"


CSRF_TRUSTED_ORIGINS = [
    origin for origin in (_as_origin(v) for v in CSRF_TRUSTED_ORIGINS) if origin
]

# ---------------------------------------------------------------------------
# Security — hardened whenever DEBUG is off.
# ---------------------------------------------------------------------------

if not DEBUG:
    # Defaults to off, not on. A clone without a .env file runs with DEBUG
    # off, and redirecting every request to https there produced a 301 loop
    # on localhost with no clue as to why. Production turns it on explicitly
    # in render.yaml, which is the only place it is actually needed.
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# ---------------------------------------------------------------------------
# Email — used for contact / volunteer / donation notifications.
# ---------------------------------------------------------------------------

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@simplygreen.or.tz")
NOTIFICATION_RECIPIENTS = env.list("NOTIFICATION_RECIPIENTS", default=[])

# ---------------------------------------------------------------------------
# Rich text editor
# ---------------------------------------------------------------------------

CKEDITOR_5_FILE_STORAGE = None
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "link", "bulletedList", "numberedList", "|",
            "blockQuote", "insertTable", "|",
            "undo", "redo",
        ],
    },
    "extends": {
        "blockToolbar": [
            "paragraph", "heading1", "heading2", "heading3", "|",
            "bulletedList", "numberedList", "|", "blockQuote",
        ],
        "toolbar": [
            "heading", "|",
            "outdent", "indent", "|",
            "bold", "italic", "link", "underline", "strikethrough", "|",
            "bulletedList", "numberedList", "todoList", "|",
            "blockQuote", "insertImage", "insertTable", "mediaEmbed", "|",
            "horizontalLine", "removeFormat", "|",
            "sourceEditing", "undo", "redo",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:alignRight",
                "imageStyle:alignCenter", "imageStyle:side", "|",
            ],
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableProperties", "tableCellProperties",
            ],
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph",
                 "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading 2",
                 "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3",
                 "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4",
                 "class": "ck-heading_heading4"},
            ]
        },
    },
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", default="INFO")},
    "loggers": {
        "django.db.backends": {"level": "WARNING", "propagate": True},
    },
}

# ---------------------------------------------------------------------------
# Unfold — modern admin UI
# ---------------------------------------------------------------------------

from django.templatetags.static import static  # noqa: E402
from django.urls import reverse_lazy  # noqa: E402


def _badge_new_submissions(request):
    """Count unread enquiries so staff see them without hunting."""
    try:
        from apps.engage.models import ContactMessage, VolunteerApplication

        return (
            ContactMessage.objects.filter(is_read=False).count()
            + VolunteerApplication.objects.filter(status="new").count()
        )
    except Exception:  # during migrations the tables may not exist yet
        return None


UNFOLD = {
    "SITE_TITLE": "Simply Green Organization",
    "SITE_HEADER": "Simply Green",
    "SITE_SUBHEADER": "Content management",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "config.settings.environment_callback",
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    "COLORS": {
        # Primary ramp generated from the logo green #99BE3D.
        "primary": {
            "50": "244 249 233",
            "100": "233 243 211",
            "200": "213 232 170",
            "300": "190 219 124",
            "400": "169 206 84",
            "500": "153 190 61",
            "600": "125 158 45",
            "700": "97 123 36",
            "800": "76 96 31",
            "900": "62 79 28",
            "950": "33 44 12",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Overview",
                "separator": False,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Site settings",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                ],
            },
            {
                "title": "About the organisation",
                "separator": True,
                "items": [
                    {"title": "Core values", "icon": "favorite",
                     "link": reverse_lazy("admin:about_corevalue_changelist")},
                    {"title": "Objectives", "icon": "flag",
                     "link": reverse_lazy("admin:about_objective_changelist")},
                    {"title": "Why partner with us", "icon": "handshake",
                     "link": reverse_lazy("admin:about_partnerreason_changelist")},
                    {"title": "Team members", "icon": "groups",
                     "link": reverse_lazy("admin:about_teammember_changelist")},
                ],
            },
            {
                "title": "Our work",
                "separator": True,
                "items": [
                    {"title": "Focus areas", "icon": "category",
                     "link": reverse_lazy("admin:programmes_focusarea_changelist")},
                    {"title": "Programmes", "icon": "eco",
                     "link": reverse_lazy("admin:programmes_programme_changelist")},
                    {"title": "Impact statistics", "icon": "insights",
                     "link": reverse_lazy("admin:core_impactstat_changelist")},
                ],
            },
            {
                "title": "News & events",
                "separator": True,
                "items": [
                    {"title": "Posts", "icon": "article",
                     "link": reverse_lazy("admin:news_post_changelist")},
                    {"title": "Categories", "icon": "label",
                     "link": reverse_lazy("admin:news_category_changelist")},
                    {"title": "Events", "icon": "event",
                     "link": reverse_lazy("admin:news_event_changelist")},
                    {"title": "Event registrations", "icon": "how_to_reg",
                     "link": reverse_lazy("admin:news_eventregistration_changelist")},
                ],
            },
            {
                "title": "Media & resources",
                "separator": True,
                "items": [
                    {"title": "Albums", "icon": "photo_library",
                     "link": reverse_lazy("admin:gallery_album_changelist")},
                    {"title": "Photos", "icon": "image",
                     "link": reverse_lazy("admin:gallery_photo_changelist")},
                    {"title": "Videos", "icon": "movie",
                     "link": reverse_lazy("admin:gallery_video_changelist")},
                    {"title": "Publications", "icon": "description",
                     "link": reverse_lazy("admin:resources_publication_changelist")},
                ],
            },
            {
                "title": "Engagement",
                "separator": True,
                "items": [
                    {"title": "Contact messages", "icon": "mail",
                     "link": reverse_lazy("admin:engage_contactmessage_changelist"),
                     "badge": "config.settings._badge_new_submissions"},
                    {"title": "Volunteers", "icon": "volunteer_activism",
                     "link": reverse_lazy("admin:engage_volunteerapplication_changelist")},
                    {"title": "Partner enquiries", "icon": "business_center",
                     "link": reverse_lazy("admin:engage_partnerenquiry_changelist")},
                    {"title": "Newsletter", "icon": "forward_to_inbox",
                     "link": reverse_lazy("admin:engage_newslettersubscriber_changelist")},
                    {"title": "Donation methods", "icon": "payments",
                     "link": reverse_lazy("admin:engage_donationmethod_changelist")},
                    {"title": "Partners & donors", "icon": "diversity_3",
                     "link": reverse_lazy("admin:core_partner_changelist")},
                ],
            },
        ],
    },
}


def environment_callback(request):
    """Show a coloured badge in the admin when this is not production."""
    import os

    name = os.environ.get("DJANGO_ENV", "development")
    if name == "production":
        return None
    return [name.title(), "warning"]


# ---------------------------------------------------------------------------
# Cache
#
# Read-only pages are cached for a few minutes. One process, one cache: this
# is a single small service, so an in-memory cache is the right size. Swap in
# Redis here if the site ever runs more than one instance.
# ---------------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "simply-green",
        "TIMEOUT": 300,
    }
}
