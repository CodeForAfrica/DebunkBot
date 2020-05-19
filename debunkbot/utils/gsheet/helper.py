import json
from typing import Optional, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.cache import cache
from django.conf import settings

from debunkbot.models import Claim


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
             eval(settings.DEBUNKBOT_GOOGLE_CREDENTIALS), strict=False)
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.__scope)
        self.__client = gspread.authorize(self.__credentials)
        self.__sheet_name = google_credentials['sheet_name']
        self.__sheet = self.__client.open(self.__sheet_name).sheet1

    def open_sheet(self) -> Optional[List[dict]]:
        """Instance method to open a workbook and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        try:
            return self.__sheet.get_all_records()
        except gspread.exceptions.SpreadsheetNotFound as e:
            return None

    def append_row(self, row_values: list) -> None:
        return self.__sheet.append_row(row_values)

    def update_cell_value(self, cell_row: int, cell_col: int, value: str) -> None:
        return self.__sheet.update_cell(cell_row, cell_col, value=value)

    def get_cell_value(self, cell_row: int, cell_col: int) -> str:
        return self.__sheet.cell(cell_row, cell_col).value

    def get_claims(self) -> Optional[List[dict]]:
        """
        Instance method that loads the claims either from the
        cache or directly from google's servers depending on whether
        we have a saved version in our cache or not
        :param self: Instance of GoogleSheetHelper
        :return: Claims
        """
        if 'claims' in cache:
            claims = cache.get('claims')
        else:
            gsheet_data = self.open_sheet()
            pos = 2
            for row in gsheet_data:            
                claim, created = Claim.objects.get_or_create(claim_first_appearance=row.get('Claim First Appearance'))
                if created:
                    claim.claim_reviewed = row.get('Claim Reviewed')
                    claim.claim_date = row.get('Claim Date')
                    claim.claim_location = row.get('Claim Location')
                    claim.url = row.get('URL')
                    claim.claim_author = row.get('Claim Author')
                    claim.rating = True if row.get('Rating').upper() == 'TRUE' else False
                    claim.sheet_row = pos
                    claim.save()
                pos+=1

            claims = Claim.objects.all()
            cache.set('claims', claims, timeout=int(getattr(settings, 'CACHE_TTL')))
        return claims
