from typing import Any, Optional, List

from django.http import HttpResponse

from debunkbot.twitter.stream_listener import Listener
from utils.gsheet.helper import GoogleSheetHelper


def write_to_gsheet(request):
    sheet = GoogleSheetHelper()
    new_row = ("Some Name", "Some Phone Number", "Some Address")
    sheet.append_row(new_row)
    sheet.update_cell_value(3, 5, 'Stargazing')
    return HttpResponse('You can confirm the write operations from your google sheet now!')


def read_gsheet(request):
    gsheet_data = GoogleSheetHelper().cache_or_load_sheet()
    return HttpResponse(f'Data from the Google Sheet {gsheet_data}')


def start_stream(request: Any) -> HttpResponse:
    data = GoogleSheetHelper().cache_or_load_sheet()  # type: Optional[List[dict]]
    links = [x.get('Claim First Appearance')
             for x in data
             if x.get('Claim First Appearance') != '' and x.get('Rating') == 'False']
    links.extend([y for x in data
                  for y in x.get('Claim Appearances').split(",")
                  if x.get('Claim Appearances') != '' and x.get('Rating') == 'False'])
    Listener().listen(links)
    return HttpResponse('All systems go!')
