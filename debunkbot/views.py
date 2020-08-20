from django.http import HttpResponse

from debunkbot.celeryapp import app
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


def fetch_gsheet_claims(request) -> HttpResponse:
    fetch_claims_from_gsheet()
    app.send_task("track_claims_task")
    return HttpResponse("Claims updated successfully")
