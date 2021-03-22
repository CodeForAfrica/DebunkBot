from __future__ import absolute_import

import os

from celery import Celery
from celery_slack import Slackify
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "debunkbot.settings")
app = Celery("debunkbot")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

SLACK_WEBHOOK = os.environ.get("DEBUNKBOT_CELERY_SLACK_WEBHOOK", "")
SLACK_WEBHOOK_FAILURES_ONLY = os.environ.get(
    "DEBUNKBOT_CELERY_SLACK_WEBHOOK_FAILURES_ONLY", ""
).strip().lower() in ("true", "t", "1")

options = {
    # Some subset of options
    "failures_only": SLACK_WEBHOOK_FAILURES_ONLY,
}
slack_app = Slackify(app, SLACK_WEBHOOK, **options)
