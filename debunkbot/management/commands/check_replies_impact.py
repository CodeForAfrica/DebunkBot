import time

from django.conf import settings
from django.core.management.base import BaseCommand

from debunkbot.models import Tweet
from debunkbot.twitter.check_reply_impact import check_reply_impact


class Command(BaseCommand):
    help = "Management command that checks the impact of our replies to debunked claims"

    def handle(self, *args, **options):
        while True:
            tweets = Tweet.objects.filter(responded=True)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Checking impact of our replies to the following tweets\n {list(tweets)}"
                )
            )
            check_reply_impact()
            for tweet in Tweet.objects.filter(responded=True):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Impact of our reply to {tweet}: \n\t {tweet.reply.impact}"
                    )
                )
            check_impact = int(settings.DEBUNKBOT_CHECK_IMPACT_INTERVAL)
            time.sleep(check_impact)
