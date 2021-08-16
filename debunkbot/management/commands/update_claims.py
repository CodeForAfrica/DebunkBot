from django.core.management.base import BaseCommand

from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Updating claims in local database..."))
        fetch_claims_from_gsheet()
        self.stdout.write(self.style.SUCCESS("Claims updated successfully"))
