"""
Django settings for Kryschendo project.
Single settings file, fully driven by environment variables via django-environ.
"""

import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Read .env file from config/ directory
env_file = BASE_DIR / "config" / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Local apps
    "main.apps.MainConfig",
    "store.apps.StoreConfig",
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
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database — parsed from DATABASE_URL env var
# Falls back to SQLite for local dev without Docker
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Los_Angeles"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT = False

# Media files — Cloud Storage in production, local in dev
gs_bucket = env("GS_BUCKET_NAME", default="")
if gs_bucket:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    }
    GS_BUCKET_NAME = gs_bucket
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Security hardening
# ---------------------------------------------------------------------------

# HTTPS / proxy — Cloud Run terminates TLS at the load balancer and forwards
# X-Forwarded-Proto: https. Trust that header so Django considers the request
# secure. Do NOT set SECURE_SSL_REDIRECT on Cloud Run (causes redirect loops).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # security: Cloud Run proxy

# HSTS — tell browsers to use HTTPS for 1 year, including subdomains, and
# submit to the preload list. Only applied when DEBUG=False.
SECURE_HSTS_SECONDS = 31536000  # security: 1 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security — cookies must only be sent over HTTPS in production.
# These are ignored in development when DEBUG=True (Django behaviour).
SESSION_COOKIE_SECURE = True  # security: HTTPS-only session cookie
CSRF_COOKIE_SECURE = True     # security: HTTPS-only CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # security: JS cannot read session cookie
CSRF_COOKIE_HTTPONLY = True     # security: JS cannot read CSRF cookie

# Clickjacking — deny embedding in iframes from other origins.
# SecurityMiddleware already sets this via XFrameOptionsMiddleware,
# but the setting must be explicitly declared to override Django's default 'SAMEORIGIN'.
X_FRAME_OPTIONS = "DENY"  # security: block iframe embedding

# Content-type sniffing — instruct browsers not to guess MIME types.
SECURE_CONTENT_TYPE_NOSNIFF = True  # security: X-Content-Type-Options: nosniff

# Legacy XSS filter header — harmless on modern browsers, defence-in-depth.
SECURE_BROWSER_XSS_FILTER = True  # security: X-XSS-Protection: 1; mode=block

# Referrer policy — send origin only on same-site requests; send only origin
# to cross-origin HTTPS destinations; send nothing to HTTP destinations.
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"  # security: limit referrer leakage

# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", default="smtp-mail.outlook.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="Kryschendo <kdl9621@hotmail.com>",
)
CONTACT_EMAIL = env("CONTACT_EMAIL", default="kdl9621@hotmail.com")

# ---------------------------------------------------------------------------
# Logging — send Django errors to stderr so Cloud Run captures them
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
