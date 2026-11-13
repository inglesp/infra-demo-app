import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be set unless DJANGO_DEBUG=1"
        )
    # For development only.
    SECRET_KEY = "django-insecure-dev-key"

ALLOWED_HOSTS = [
    host for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if host
]

INSTALLED_APPS = ["counter"]

# Django only checks a request's host against ALLOWED_HOSTS when something calls
# request.get_host(). CommonMiddleware does this for every request, so without
# it, requests for any host would be answered.
#
# Dokku's health checks call the container directly, without the app's domain,
# so the health check middleware must come first, to answer them before the
# host is checked.
MIDDLEWARE = [
    "config.middleware.health_check",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DATABASE_PATH", BASE_DIR / "db.sqlite3"),
    }
}

GIT_COMMIT = os.environ.get("GIT_COMMIT", "unknown")

# A secret with no use, which the page shows, to show that secrets reach the
# app. Never show a real secret like this.
DEMO_SECRET = os.environ.get("DEMO_SECRET", "")

# A value with no use, which the page shows, to show that non-secret config
# reaches the app.
DEMO_NON_SECRET = os.environ.get("DEMO_NON_SECRET", "")

# Send all logs, including Django's, to stderr, where Docker collects them.
# Django's default config only writes to the console when DEBUG is on, and
# otherwise emails ADMINS, so without this, errors in views would be lost.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{levelname}] {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        # Replaces Django's default handlers for this logger
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

USE_TZ = True
