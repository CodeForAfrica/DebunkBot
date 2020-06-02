from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from debunkbot.utils.gsheet.helper import GoogleSheetHelper

from debunkbot.models import Message


class Command(BaseCommand):
    help = 'Management command that checks the impact of our replies to debunked claims'

    def handle(self, *args, **options):
        messages = Message.objects.all()
        gsheet_helper = GoogleSheetHelper()
        print(gsheet_helper.fetch_response_messages())