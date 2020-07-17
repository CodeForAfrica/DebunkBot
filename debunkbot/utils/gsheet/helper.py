import json
import logging
from typing import Optional, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.cache import cache
from django.conf import settings

from debunkbot.models import Claim, MessageTemplate, MessageTemplateSource, GoogleSheetCredentials

logger = logging.getLogger(__name__)


class GoogleSheetHelper(object):
    """Helper class for getting data from google sheet"""

    def __init__(self) -> None:
        """Instance method to initialize Google Drive API
        :param self:
        :return: None
        """
        self.__scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = GoogleSheetCredentials.objects.first()
        if credentials:
            google_credentials = GoogleSheetCredentials.objects.first().credentials
        else:
            raise Exception("Google credentials have not been set up.")
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.__scope)
        self.__client = gspread.authorize(self.__credentials)    
    
    def get_sheet(self, sheet_key):
        return self.__client.open_by_key(sheet_key)
        
    def open_work_sheet(self, sheet_id, work_sheet_name) -> Optional[List[dict]]:
        """Instance method to open a worksheet and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        sheet = self.get_sheet(sheet_id)
        worksheet = sheet.worksheet(work_sheet_name)
        try:
            return worksheet.get_all_records()
        except gspread.exceptions.SpreadsheetNotFound as e:
            return None

    def get_claims(self) -> Optional[List[dict]]:
        """
        Instance method that loads the claims either from the
        cache or directly from google's servers depending on whether
        we have a saved version in our cache or not
        :param self: Instance of GoogleSheetHelper
        :return: Claims
        """
        claims = Claim.objects.all()
        return claims
    
    def fetch_response_messages(self):
        # Delete all existing messages and create new ones.
        MessageTemplate.objects.all().delete()

        message_template_sources = MessageTemplateSource.objects.all()
        message_templates = []

        for message_template_source in message_template_sources:
            try:
                sheet = self.get_sheet(message_template_source.key).worksheet(message_template_source.worksheet)
                response_message_templates = sheet.get_all_records()
                for response_message_template in response_message_templates:
                    message_template = response_message_template.get(message_template_source.column)
                    if message_template and message_template != '':
                            message_templates.append(MessageTemplate(message_template=message_template, message_template_source=message_template_source))
            except Exception as error:
                continue

        MessageTemplate.objects.bulk_create(message_templates)
