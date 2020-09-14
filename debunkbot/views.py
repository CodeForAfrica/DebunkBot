from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from debunkbot.celeryapp import app
from debunkbot.serializers import ClaimSerializer
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


@api_view(["GET", "POST"])
@authentication_classes(
    [TokenAuthentication,]
)
@permission_classes(
    [IsAuthenticated,]
)
def handle_claims(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ClaimSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    fetch_claims_from_gsheet()
    app.send_task("track_claims_task")
    return HttpResponse("Claims fetched successfully")
