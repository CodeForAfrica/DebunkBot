import time
import tweepy
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings

from debunkbot.utils.claims_handler import fetch_claims_from_gsheet
from debunkbot.celeryapp import app


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Updating claims in local database...'))
        fetch_claims_from_gsheet()
        self.stdout.write(self.style.SUCCESS(f'Claims updated successfully'))
        self.stdout.write(self.style.NOTICE(f'Restarting stream listener...'))
        app.send_task('track_claims_task')
        self.stdout.write(self.style.SUCCESS(f'Stream listener restarted.'))
