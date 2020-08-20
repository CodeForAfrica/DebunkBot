from django.core.management.base import BaseCommand

from debunkbot.utils.gsheet.helper import GoogleSheetHelper


class Command(BaseCommand):
    help = "Management command that fetches messages to use while sending out responses"

    def handle(self, *args, **options):
        gsheet_helper = GoogleSheetHelper()
        gsheet_helper.fetch_response_messages()
