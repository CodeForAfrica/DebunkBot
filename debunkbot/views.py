from typing import Optional, List

from django.http import HttpResponse

from debunkbot.twitter.process_stream import process_stream
from debunkbot.twitter.stream_listener import stream
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


def start_stream(request) -> HttpResponse:
    data = GoogleSheetHelper().cache_or_load_sheet()  # type: Optional[List[dict]]
    links = [x.get('Claim First Appearance')
             for x in data
             if x.get('Claim First Appearance') != '' and x.get('Rating').lower() == 'false']
    # links.extend([y.strip() for x in data
    #               for y in x.get('Claim Appearances').split(",")
    #               if x.get('Claim Appearances') != '' and x.get('Rating').lower() == 'false'])
    # links.append('asciidev')
    print(links, flush=True)
    stream(links)
    return HttpResponse('All systems go!')


def process(request) -> HttpResponse:
    process_stream()
    return HttpResponse('Cappuccino')
