import json
from typing import Optional, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.cache import cache
from django.conf import settings

from debunkbot.models import Claim, MessageTemplate


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
        google_credentials = json.loads(
            settings.DEBUNKBOT_GOOGLE_CREDENTIALS, strict=False)
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.__scope)
        self.__client = gspread.authorize(self.__credentials)
        self.__sheet_name = google_credentials['sheet_name']
        
    def get_work_sheet(self, work_sheet_name=settings.DEBUNKBOT_BOT_CLAIMS_WORKSPACE):
        return self.__client.open(self.__sheet_name).worksheet(work_sheet_name)

    def open_work_sheet(self, work_sheet_name=settings.DEBUNKBOT_BOT_CLAIMS_WORKSPACE) -> Optional[List[dict]]:
        """Instance method to open a workbook and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        sheet = self.get_work_sheet(work_sheet_name)
        try:
            return sheet.get_all_records()
        except gspread.exceptions.SpreadsheetNotFound as e:
            return None

    def append_row(self, row_values: list) -> None:
        sheet = self.get_work_sheet()
        return sheet.append_row(row_values)

    def update_cell_value(self, cell_row: int, cell_col: int, value: str) -> None:
        sheet = self.get_work_sheet()
        return sheet.update_cell(cell_row, cell_col, value=value)

    def get_cell_value(self, cell_row: int, cell_col: int) -> str:
        sheet = self.get_work_sheet()
        return sheet.cell(cell_row, cell_col).value
    
    def populate_claim_object(self, row, claim):
        claim.claim_reviewed = row.get(settings.DEBUNKBOT_BOT_CLAIM_REVIEWED_COLUMN) or "N/A"
        claim.claim_date = row.get(settings.DEBUNKBOT_BOT_CLAIM_DATE_COLUMN) or "N/A"
        claim.claim_location = row.get(settings.DEBUNKBOT_BOT_CLAIM_LOCATION_COLUMN) or "N/A"
        claim.fact_checked_url = row.get(settings.DEBUNKBOT_BOT_FACT_CHECKED_URL_COLUMN) or "N/A"
        claim.claim_author = row.get(settings.DEBUNKBOT_BOT_CLAIM_AUTHOR_COLUMN) or "Unknown"
        return claim

    def get_claims(self) -> Optional[List[dict]]:
        """
        Instance method that loads the claims either from the
        cache or directly from google's servers depending on whether
        we have a saved version in our cache or not
        :param self: Instance of GoogleSheetHelper
        :return: Claims
        """
        claims = cache.get('claims')
        if not claims:
            gsheet_data = self.open_work_sheet()
            pos = 2
            for row in gsheet_data:
                claim_first_appearance = row.get(settings.DEBUNKBOT_BOT_CLAIM_FIRST_APPEARANCE_COLUMN)
                claim_phrase = row.get(settings.DEBUNKBOT_BOT_CLAIM_PHRASE_COLUMN)
                conclusion = row.get(settings.DEBUNKBOT_BOT_CLAIM_CONCLUSION_COLUMN)
                
                if claim_first_appearance:
                    claim, created = Claim.objects.get_or_create(claim_first_appearance=claim_first_appearance[:255])
                elif claim_phrase:
                    claim, created = Claim.objects.get_or_create(claim_phrase=claim_phrase[:255])
                else:
                    # Tracking rows are missing so we should skip this row.
                    pos+=1
                    continue

                if created:
                    claim = self.populate_claim_object(row, claim)

                if conclusion.upper() == 'FALSE':
                    claim.rating = False
                elif conclusion.upper() == 'TRUE':
                    claim.rating = True
                else:
                    # Skip this claim since we don't know if it is true or false
                    pos+=1
                    claim.delete()
                    continue
                claim.sheet_row = pos
                claim.save()
                pos+=1

            claims = Claim.objects.all()
            cache.set('claims', claims, timeout=int(settings.DEBUNKBOT_CACHE_TTL))
        return claims
    
    def fetch_response_messages(self):
        # Delete all existing messages and create new ones.
        MessageTemplate.objects.all().delete()
        response_message_templates = self.open_work_sheet(settings.DEBUNKBOT_BOT_RESPONSES_WORKSPACE)
        message_templates = [MessageTemplate(
            message_template=response_message_template.get(settings.DEBUNKBOT_BOT_RESPONSES_COLUMN)
        ) for response_message_template in response_message_templates]
        MessageTemplate.objects.bulk_create(message_templates)
