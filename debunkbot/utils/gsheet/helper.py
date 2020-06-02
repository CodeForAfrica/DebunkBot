import json
from typing import Optional, List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.cache import cache
from django.conf import settings

from debunkbot.models import Claim, Message


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
        # google_credentials = json.loads(
        #      eval(settings.DEBUNKBOT_GOOGLE_CREDENTIALS), strict=False)
        google_credentials = json.loads(
            settings.DEBUNKBOT_GOOGLE_CREDENTIALS, strict=False)
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.__scope)
        self.__client = gspread.authorize(self.__credentials)
        self.__sheet_name = google_credentials['sheet_name']
        self.__sheet = self.__client.open(self.__sheet_name).worksheet('KENYA')

    def open_work_sheet(self, work_sheet_name) -> Optional[List[dict]]:
        """Instance method to open a workbook and get the data
        in Space Allocation sheet
        :param self: Instance of GoogleSheetHelper
        :return: Sheet Record as dict or None
        """
        sheet = self.__client.open(self.__sheet_name).worksheet(work_sheet_name)
        try:
            return sheet.get_all_records()
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
        claims = cache.get('claims')
        if not claims:
            gsheet_data = self.open_work_sheet("KENYA")
            pos = 2
            for row in gsheet_data:
                claim_first_appearance = row.get('Claim First Appearance')
                claim_phrase = row.get('Claim Phrase')

                if claim_first_appearance:
                    claim, created = Claim.objects.get_or_create(claim_first_appearance=claim_first_appearance[:255])
                elif claim_phrase:
                    claim, created = Claim.objects.get_or_create(claim_phrase=claim_phrase[:255])
                else:
                    # The two tracking rows are missing so we should skip this row.
                    pos+=1
                    continue

                if created:
                    claim.claim_reviewed = row.get('Claim Reviewed')
                    claim.claim_date = row.get('Claim Date')
                    claim.claim_location = row.get('Claim Location') or "KENYA"
                    claim.fact_checked_url = row.get('Fact Checked URL')
                    claim.claim_author = row.get('Claim Author') or "Unknown"
                    conclusion = row.get('Conclusion')
                    
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
    
    def get_links(self):
        """
            Returns a list of links from all the claims that we have.
        """
        links = []
        # This will most of the times get the cached claims so no network calls will be made.
        for claim in self.get_claims():
            if claim.claim_first_appearance:
                url_link = claim.claim_first_appearance
                if url_link != '' and not claim.rating:
                    url_link = url_link.split("://")[-1]
                    url_link = url_link.split("www.")[-1]
                    url_link = url_link.split("mobile.")[-1]
                    url_link = url_link.split("web.")[-1]
                    url_link = url_link.split("docs.")[-1]
                    
                    url_link = url_link.split("/")
                    # Replace the . with a space
                    domain_part = url_link[0].split('.')
                    url_link = domain_part+url_link[1:]
                    url_parts = ' '.join(url_link)
                    url_parts = ' '.join(' '.join(' '.join(' '.join(url_parts.split('?')).split('.')).split('=')).split('&'))
                    # Pick the first 60 words of the new url.
                    all_parts = url_parts.split(' ')
                    current_filter = ''
                    for part in all_parts:
                        if len(current_filter) < 60 and len(current_filter+part) < 60:
                            current_filter +=part+" "
                        else:
                            break
                    current_filter = ' '.join(current_filter.split('?'))
                    links.append(current_filter.strip())     
            elif claim.claim_phrase and not claim.rating:
                links.append(claim.claim_phrase[:60])
            else:
                # We don't have anything to tack on this claim
                continue
        return links
    
    def fetch_response_messages(self):
        # Delete all existing messages and create new ones.
        Message.objects.all().delete()
        response_messages = self.open_work_sheet(settings.DEBUNKBOT_BOT_RESPONSES_WORKSPACE)
        messages = [Message(
            message=message.get(settings.DEBUNKBOT_BOT_RESPONSES_COLUMN)
        ) for message in response_messages]
        Message.objects.bulk_create(messages)
