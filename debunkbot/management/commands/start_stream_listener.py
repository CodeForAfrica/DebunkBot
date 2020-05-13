import tweepy
from django.core.management.base import BaseCommand, CommandError

from utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    help = 'Management command that starts the stream listener'

    def handle(self, *args, **options):
        data = GoogleSheetHelper().cache_or_load_sheet()
        links = [x.get('Claim First Appearance')
             for x in data
             if x.get('Claim First Appearance') != '' and x.get('Rating').lower() == 'false']
        
        self.stdout.write(self.style.SUCCESS(f'Starting stream listener for the following URLs \n {links}'))
        stream(links)
