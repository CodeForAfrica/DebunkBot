from django.core.management.base import BaseCommand

from debunkbot.twitter.process_stream import process_stream


class Command(BaseCommand):
    help = "Management command that sends replies to tweets with debunked urls"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Sending reply to selected tweet."))
        process_stream()
        self.stdout.write(self.style.SUCCESS("Done sending reply"))
