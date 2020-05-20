import time
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from debunkbot.models import Tweet
from debunkbot.twitter.process_stream import process_stream


class Command(BaseCommand):
    help = 'Management command that sends replies to tweets with debunked urls'

    def handle(self, *args, **options):
        while True:
            un_replied_tweets = Tweet.objects.filter(processed=False)
            self.stdout.write(self.style.SUCCESS(f'Sending replies to the following tweets \n {un_replied_tweets}'))
            process_stream()
            self.stdout.write(self.style.SUCCESS(f'Done sending replies'))
            refresh_tracklist_timeout = int(settings.SEND_REPLIES_AFTER)
            time.sleep(refresh_tracklist_timeout)
