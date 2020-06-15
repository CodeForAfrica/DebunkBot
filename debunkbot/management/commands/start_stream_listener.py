import time
import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.utils.links_handler import get_links
from debunkbot.utils.claims_handler import retrieve_claims_from_db
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    help = 'Management command that starts the stream listener'

    def handle(self, *args, **options):
        links = get_links(retrieve_claims_from_db()) 
        self.stdout.write(self.style.SUCCESS(f'Stream listener running..'))
        stream(links)
