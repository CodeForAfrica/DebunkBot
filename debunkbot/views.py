from django.http import HttpResponse

from utils.gsheet.helper import GoogleSheetHelper


def write_to_gsheet(request):
    sheet = GoogleSheetHelper()
    new_row = ("Some Name", "Some Phone Number", "Some Address")
    sheet.append_row(new_row)
    sheet.update_cell_value(3, 5, 'Stargazing')
    return HttpResponse('You can confirm the write operations from your google sheet now!')
