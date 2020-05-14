import time
import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    help = 'Management command that starts the stream listener'

    def handle(self, *args, **options):
        while True:
            data = GoogleSheetHelper().cache_or_load_sheet()
            links = []
            for link in data:
                url_link = link.get('Claim First Appearance')
                if  url_link != '' and link.get('Rating').lower() == 'false':
                    if len(url_link) > 60:
                        url_link = url_link.split("www.")[-1]
                        links.append(url_link)
                        if len(url_link) > 60:
                            url_link = url_link.split("/")[1]
                            links.extend(url_link)
                    else:
                        links.append(url_link)
        
            self.stdout.write(self.style.SUCCESS(f'Stream listener running..'))
            stream(links)
            time.sleep(2)
