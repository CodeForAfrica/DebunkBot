import time
import tweepy
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings

from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            gsheet = GoogleSheetHelper()
            gsheet_data = gsheet.open_sheet()

            pos = 2
            for row in gsheet_data:
                row.update({'row': pos})
                pos+=1
            
            cache.set('gsheet_data', gsheet_data, timeout=0)
            self.stdout.write(self.style.SUCCESS(f'Refreshing google sheet data...'))
            refresh_tracklist_timeout = int(settings.REFRESH_TRACK_LIST_TIMEOUT)
            if refresh_tracklist_timeout > 60:
                time.sleep(refresh_tracklist_timeout - 60)
            else:
                time.sleep(refresh_tracklist_timeout)
