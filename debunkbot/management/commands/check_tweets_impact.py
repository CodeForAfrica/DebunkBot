import time
import tweepy
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from debunkbot.twitter.check_tweet_impact import check_tweet_impact
from debunkbot.models import Tweet


class Command(BaseCommand):
    help = 'Management command that checks the impact of tweets sharing misinformation.'

    def handle(self, *args, **options):
        while True:
            tweets = Tweet.objects.filter(processed=False, deleted=False)
            self.stdout.write(self.style.SUCCESS(f'Checking impact of the following tweets\n {list(tweets)}'))
            check_tweet_impact()
            check_impact = int(settings.DEBUNKBOT_CHECK_IMPACT)
            time.sleep(check_impact)
