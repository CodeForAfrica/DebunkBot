import json
import os
from typing import Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetHelper(object):
    """Helper class for getting data from google sheet"""

    def __init__(self):
        """Instance method to initialize Google Drive API
        :param self:
        :return: None
        """
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        google_credentials = json.loads(
            os.getenv('GOOGLE_CREDENTIALS'), strict=False)
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.scope)
        self.client = gspread.authorize(self.credentials)

    def open_sheet(self) -> Optional[dict]:
        """Instance method to open a workbook and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        try:
            sheet = self.client.open(os.getenv('GOOGLE_SHEET_NAME')).sheet1
            return sheet.get_all_records()

        except gspread.exceptions.SpreadsheetNotFound as e:
            return None
