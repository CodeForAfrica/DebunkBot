import time

from django.conf import settings
from django.core.management.base import BaseCommand

from debunkbot.models import Tweet
from debunkbot.twitter.check_tweets_metrics import check_tweets_metrics


class Command(BaseCommand):
    help = "Management command that checks the impact of tweets sharing misinformation."

    def handle(self, *args, **options):
        while True:
            tweets = Tweet.objects.filter(processed=False, deleted=False)
            check_tweets_metrics(tweets)
            check_impact = int(settings.DEBUNKBOT_CHECK_IMPACT_INTERVAL)
            time.sleep(check_impact)
