from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debunkbot.settings")

# The Intervals should be in minutes.
DEBUNKBOT_RESPONSE_INTERVAL = settings.DEBUNKBOT_RESPONSE_INTERVAL
DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL = (
    settings.DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL
)
DEBUNKBOT_CHECK_IMPACT_INTERVAL = settings.DEBUNKBOT_CHECK_IMPACT_INTERVAL
DEBUNKBOT_FETCH_RESPONSES_MESSAGES_INTERVAL = (
    settings.DEBUNKBOT_FETCH_RESPONSES_MESSAGES_INTERVAL
)
DEBUNKBOT_PULL_CLAIMS_INTERVAL = settings.DEBUNKBOT_PULL_CLAIMS_INTERVAL
DEBUNKBOT_UPDATE_GSHEET_INTERVAL = settings.DEBUNKBOT_UPDATE_GSHEET_INTERVAL
DEBUNKBOT_SEARCH_CLAIMS_INTERVAL = settings.DEBUNKBOT_SEARCH_CLAIMS_INTERVAL

app = Celery("debunkbot")
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True

app.conf.beat_schedule = {
    "pull_claims_from_gsheet": {
        "task": "pull_claims_from_gsheet",
        "schedule": crontab(minute=0, hour=f"*/{DEBUNKBOT_PULL_CLAIMS_INTERVAL}"),
    },
    "fetch_bot_response_messages": {
        "task": "fetch_response_messages",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_FETCH_RESPONSES_MESSAGES_INTERVAL}"),
    },
    "update_debunkbot_google_sheet": {
        "task": "update_debunkbot_google_sheet",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_UPDATE_GSHEET_INTERVAL}"),
    },
    "check_tweet_metrics": {
        "task": "check_tweet_metrics",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL}"),
    },
    "search_claims": {
        "task": "search_claims",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_SEARCH_CLAIMS_INTERVAL}"),
    },
    "send_replies_task": {
        "task": "send_replies_task",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_RESPONSE_INTERVAL}"),
    },
    "check_replies_impact": {
        "task": "check_replies_impact",
        "schedule": crontab(minute=f"*/{DEBUNKBOT_CHECK_IMPACT_INTERVAL}"),
    },
}
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
