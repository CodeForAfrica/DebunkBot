from django.http import HttpResponse
from django.core.cache import cache

from debunkbot.utils.claims_handler import fetch_claims_from_gsheet
from debunkbot.tasks import stream_listener
from debunkbot.celery import app


def fetch_gsheet_claims(request) -> HttpResponse:
    fetch_claims_from_gsheet()
    app.send_task(cache.get('task_name', 'start_stream_listener_task'))
    return HttpResponse('Claims updated successfully')
