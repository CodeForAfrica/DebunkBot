import json
import os
from typing import Optional, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.cache import cache
from django.conf import settings


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
            eval(os.getenv('GOOGLE_CREDENTIALS')), strict=False)
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

    def update_cell_value(self, cell_row: int, cell_col: int, value: str) -> str:
        return self.__sheet.update_cell(cell_row, cell_col, value=value)

    def get_cell_value(self, cell: str) -> str:
        return self.__sheet.acell(cell).value

    def cache_or_load_sheet(self) -> Optional[List[dict]]:
        """
        Instance method that loads the google sheet either from the
        cache or directly from google's servers depending on whether
        we have a saved version in our cache or not
        :param self: Instance of GoogleSheetHelper
        :return: Sheet record as dict or None
        """
        if 'gsheet_data' in cache:
            gsheet_data = cache.get('gsheet_data')
        else:
            gsheet_data = self.open_sheet()
            cache.set('gsheet_data', gsheet_data, timeout=int(getattr(settings, 'CACHE_TTL')))
        return gsheet_data
