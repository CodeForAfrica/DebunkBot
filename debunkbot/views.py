from django.http import HttpResponse

from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


def fetch_gsheet_claims(request) -> HttpResponse:
    fetch_claims_from_gsheet()
    return HttpResponse('All systems go!')
