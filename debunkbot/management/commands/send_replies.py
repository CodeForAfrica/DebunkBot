import time
from django.core.management.base import BaseCommand
from django.conf import settings

from debunkbot.twitter.process_stream import process_stream


class Command(BaseCommand):
    help = 'Management command that sends replies to tweets with debunked urls'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Sending reply to selected tweet'))
        process_stream()
        self.stdout.write(self.style.SUCCESS(f'Done sending reply'))
        # refresh_tracklist_timeout = int(settings.DEBUNKBOT_RESPONSE_INTERVAL)
        # time.sleep(refresh_tracklist_timeout)
