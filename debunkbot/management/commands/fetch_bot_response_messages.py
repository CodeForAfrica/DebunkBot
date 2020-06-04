from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from debunkbot.utils.gsheet.helper import GoogleSheetHelper

from debunkbot.models import MessageTemplate


class Command(BaseCommand):
    help = 'Management command that fetches messages to use while sending out responses'

    def handle(self, *args, **options):
        gsheet_helper = GoogleSheetHelper()
        gsheet_helper.fetch_response_messages()
