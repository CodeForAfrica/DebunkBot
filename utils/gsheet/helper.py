import json
import os
from typing import Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        credentials = os.getenv('GOOGLE_CREDENTIALS')
        if not credentials:
            raise ValueError("GOOGLE_CREDENTIALS must be set as an environment variable.")
        google_credentials = json.loads(
            credentials, strict=False)
        sheet_name = google_credentials.get('sheet_name')
        if not sheet_name:
            raise ValueError("Sheet name has not been set in the GOOGLE_CREDENTIALS environment variable.")
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.__scope)
        self.__client = gspread.authorize(self.__credentials)
        self.__sheet_name = sheet_name
        self.__sheet = self.__client.open(self.__sheet_name).sheet1

    def open_sheet(self) -> Optional[dict]:
        """Instance method to open a workbook and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        try:
            return self.__sheet.get_all_records()
        except gspread.exceptions.SpreadsheetNotFound as e:
            return None

    def append_row(self, row_values):
        return self.__sheet.append_row(row_values)

    def update_cell_value(self, cell_row, cell_col, value):
        return self.__sheet.update_cell(cell_row, cell_col, value=value)
