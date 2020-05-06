from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from utils.gsheet.helper import GoogleSheetHelper


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def write_to_gsheet(request):
    sheet = GoogleSheetHelper()
    new_row = ("Some Name", "Some Phone Number", "Some Address")
    sheet.append_row(new_row)
    sheet.update_cell_value(3, 5, 'Stargazing')
    return HttpResponse('You can confirm the write operations from your google sheet now!')

def read_gsheet(request):
    if 'gsheet_data' in cache:
        gsheet_data = cache.get('gsheet_data')
    else:
        sheet_helper = GoogleSheetHelper()
        gsheet_data = sheet_helper.open_sheet()
        cache.set('gsheet_data', gsheet_data, timeout=CACHE_TTL)
    
    return HttpResponse(f'Data from the Google Sheet {gsheet_data}')
