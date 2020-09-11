from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from debunkbot.celeryapp import app
from debunkbot.serializers import ClaimSerializer
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


def fetch_gsheet_claims(request) -> HttpResponse:
    fetch_claims_from_gsheet()
    app.send_task("track_claims_task")
    return HttpResponse("Claims updated successfully")


@api_view(["POST"])
def handle_claims_post(request):
    data = JSONParser().parse(request)
    serializer = ClaimSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
