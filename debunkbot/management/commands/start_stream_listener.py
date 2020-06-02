import time
import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    help = 'Management command that starts the stream listener'

    def handle(self, *args, **options):
        while True:
            links = GoogleSheetHelper().get_links() 
            
            self.stdout.write(self.style.SUCCESS(f'Stream listener running..'))
            x = list(set(links))
            stream(x)
            time.sleep(10)
