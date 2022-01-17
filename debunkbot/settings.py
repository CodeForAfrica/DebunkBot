"""
Django settings for debunkbot project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path  # python3 only

import dj_database_url
import sentry_sdk
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from dotenv import load_dotenv
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "#24qq32j=!zxp4s7_h3%h9ag0z0*c13t0y2gu3sk6c!tomn^_0"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", True)

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Sentry setup
DEBUNKBOT_SENTRY_DSN = os.getenv("DEBUNKBOT_SENTRY_DSN")
sentry_sdk.init(
    dsn=DEBUNKBOT_SENTRY_DSN,
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debunkbot",
    "rest_framework",
    "rest_framework.authtoken",
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

ROOT_URLCONF = "debunkbot.urls"

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

WSGI_APPLICATION = "debunkbot.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://debunkbot:debunkbot@db:5432/debunkbot",
)
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DEBUNKBOT_REDIS_LOCATION = os.getenv("DEBUNKBOT_REDIS_LOCATION", "redis://redis:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": DEBUNKBOT_REDIS_LOCATION,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

DEBUNKBOT_CACHE_TTL = os.getenv("DEBUNKBOT_CACHE_TTL", DEFAULT_TIMEOUT)
TWITTER_CLIENT_KEY = os.getenv("DEBUNKBOT_TWITTER_CLIENT_KEY")
TWITTER_CLIENT_SECRET = os.getenv("DEBUNKBOT_TWITTER_CLIENT_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("DEBUNKBOT_TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("DEBUNKBOT_TWITTER_ACCESS_SECRET")

DEFAULT_INTERVAL = 60

# Amount of time to wait before sending replies to tweets with debunked urls.
DEBUNKBOT_RESPONSE_INTERVAL = os.getenv("DEBUNKBOT_RESPONSE_INTERVAL", DEFAULT_INTERVAL)

# Amount of time to wait before checking the impact of our reply to tweets with debunked
# urls.
DEBUNKBOT_CHECK_IMPACT_INTERVAL = os.getenv(
    "DEBUNKBOT_CHECK_IMPACT_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_PULL_CLAIMS_INTERVAL = os.getenv(
    "DEBUNKBOT_PULL_CLAIMS_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_UPDATE_GSHEET_INTERVAL = os.getenv(
    "DEBUNKBOT_UPDATE_GSHEET_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL = os.getenv(
    "DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_FETCH_RESPONSES_MESSAGES_INTERVAL = os.getenv(
    "DEBUNKBOT_FETCH_RESPONSES_MESSAGES_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_SEARCH_CLAIMS_INTERVAL = os.getenv(
    "DEBUNKBOT_SEARCH_CLAIMS_INTERVAL", DEFAULT_INTERVAL
)

DEBUNKBOT_GSHEET_ID = os.getenv("DEBUNKBOT_GSHEET_ID")
DEBUNKBOT_GSHEET_CLAIM_RATINGS = os.getenv("DEBUNKBOT_GSHEET_CLAIM_RATINGS", "")
# from which row to start reading the claims
DEBUNKBOT_GSHEET_ROW_HEAD = os.getenv("DEBUNKBOT_GSHEET_ROW_HEAD", 1)

TWITTER_SEARCH_LIMIT = os.getenv("TWITTER_SEARCH_LIMIT", 100)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REST_FRAMEWORK
REST_FRAMEWORK = {
    "DATE_INPUT_FORMATS": [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%b %d %Y",
        "%b %d, %Y",
        "%d %b %Y",
        "%d %b, %Y",
        "%B %d %Y",
        "%B %d, %Y",
        "%d %B %Y",
        "%d %B, %Y",
        "%d.%m.%Y",
    ],
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Recheck the filesystem to see if any files have changed before responding.
WHITENOISE_AUTOREFRESH = True

# CELERY STUFF
BROKER_URL = os.getenv("DEBUNKBOT_BROKER_URL", "redis://redis:6379")
CELERY_RESULT_BACKEND = os.getenv(
    "DEBUNKBOT_CELERY_RESULT_BACKEND", "redis://redis:6379"
)
CELERY_ACCEPT_CONTENT = os.getenv(
    "DEBUNKBOT_CELERY_ACCEPT_CONTENT", "application/json"
).split(",")
CELERY_TASK_SERIALIZER = os.getenv("DEBUNKBOT_CELERY_TASK_SERIALIZER", "json")
CELERY_RESULT_SERIALIZER = os.getenv("DEBUNKBOT_CELERY_RESULT_SERIALIZER", "json")
CELERY_TIMEZONE = os.getenv("DEBUNKBOT_CELERY_TIMEZONE", "Africa/Nairobi")
DEBUNKBOT_CELERY_SLACK_WEBHOOK = os.getenv("DEBUNKBOT_CELERY_SLACK_WEBHOOK", "")
DEBUNKBOT_CELERY_SLACK_WEBHOOK_FAILURES_ONLY = os.getenv(
    "DEBUNKBOT_CELERY_SLACK_WEBHOOK_FAILURES_ONLY", ""
)

SENDGRID_API_KEY = os.getenv("DEBUNKBOT_SENDGRID_API_KEY", "")

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
