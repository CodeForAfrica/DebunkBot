"""
Django settings for debunkbot project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import dj_database_url
from django.core.cache.backends.base import DEFAULT_TIMEOUT

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '#24qq32j=!zxp4s7_h3%h9ag0z0*c13t0y2gu3sk6c!tomn^_0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "*"
).split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debunkbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'debunkbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'debunkbot.wsgi.application'


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
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEBUNKBOT_REDIS_LOCATION = os.getenv('DEBUNKBOT_REDIS_LOCATION', "redis://127.0.0.1:6379/1")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": DEBUNKBOT_REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

DEBUNKBOT_CACHE_TTL = os.getenv('DEBUNKBOT_CACHE_TTL', DEFAULT_TIMEOUT)
TWITTER_CLIENT_KEY = os.getenv('DEBUNKBOT_TWITTER_CLIENT_KEY')
TWITTER_CLIENT_SECRET = os.getenv('DEBUNKBOT_TWITTER_CLIENT_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('DEBUNKBOT_TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('DEBUNKBOT_TWITTER_ACCESS_SECRET')

# Amount of time to wait before refreshing the track list with new data from the google sheet
DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT = os.getenv('DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT')

# Amount of time to wait before sending replies to tweets with debunked urls.
DEBUNKBOT_RESPONSE_INTERVAL = os.getenv('DEBUNKBOT_RESPONSE_INTERVAL')

# Amount of time to wait before checking the impact of our reply to tweets with debunked urls.
DEBUNKBOT_CHECK_IMPACT_INTERVAL = os.getenv('DEBUNKBOT_CHECK_IMPACT_INTERVAL')

DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL = os.getenv('DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL')

DEBUNKBOT_BOT_UPDATE_GSHEET_INTERVAL = os.getenv('DEBUNKBOT_BOT_UPDATE_GSHEET_INTERVAL')

DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL = os.getenv('DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL')

DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL = os.getenv('DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL')

DEBUNKBOT_GSHEET_ID = os.getenv('DEBUNKBOT_GSHEET_ID')

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


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
BROKER_URL = os.getenv('DEBUNKBOT_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('DEBUNKBOT_CELERY_RESULT_BACKEND', 'redis://localhost:6379')
CELERY_ACCEPT_CONTENT = os.getenv("DEBUNKBOT_CELERY_ACCEPT_CONTENT", "application/json").split(",")
CELERY_TASK_SERIALIZER = os.getenv("DEBUNKBOT_CELERY_TASK_SERIALIZER", 'json')
CELERY_RESULT_SERIALIZER = os.getenv("DEBUNKBOT_CELERY_RESULT_SERIALIZER", 'json')
CELERY_TIMEZONE = os.getenv("DEBUNKBOT_CELERY_TIMEZONE", 'Africa/Nairobi')
