import time
import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.utils.gsheet import debunk_bot_gsheet_helper


class Command(BaseCommand):
    help = 'Management command that updates the debunk bot google sheet'

    def handle(self, *args, **options):        
        self.stdout.write(self.style.SUCCESS(f'Starting the UPDATE...'))
        debunk_bot_gsheet_helper.update_debunkbot_gsheet()
        self.stdout.write(self.style.SUCCESS(f'Update Complete.'))
