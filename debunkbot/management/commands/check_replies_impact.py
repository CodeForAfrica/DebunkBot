import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.twitter.check_reply_impact import check_reply_impact
from debunkbot.models import Tweet


class Command(BaseCommand):
    help = 'Management command that checks the impact of our replies to debunked claims'

    def handle(self, *args, **options):
        tweets = Tweet.objects.filter(responded=True)
        self.stdout.write(self.style.SUCCESS(f'Checking impact of our replies to the following tweets\n {list(tweets)}'))
        check_reply_impact()
        for tweet in Tweet.objects.filter(responded=True):
            self.stdout.write(self.style.SUCCESS(f'Impact of our reply to {tweet}: \n\t {tweet.impact}'))
