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

from debunkbot.models import ClaimsTracker
from debunkbot.serializers import ClaimSerializer, ClaimsTrackerSerializer
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet


@api_view(["GET", "POST"])
@authentication_classes(
    [
        TokenAuthentication,
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def handle_claims(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ClaimSerializer(data=data)
        if serializer.is_valid():
            instance, created = serializer.get_or_create()
            if not created:
                serializer.update(instance, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    fetch_claims_from_gsheet()
    return HttpResponse("Claims fetched successfully")


@api_view(["GET", "PUT"])
@authentication_classes(
    [
        TokenAuthentication,
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def claims_tracker(request, claims_db):
    claims_tracker = ClaimsTracker.objects.filter(claim_db=claims_db).first()
    if request.method == "GET":
        claims_tracker_serializer = ClaimsTrackerSerializer(claims_tracker)
        if claims_tracker is None:
            # Create the claims_tracker
            claims_tracker_serializer = ClaimsTrackerSerializer(
                data={"claim_db": claims_db}
            )
            if claims_tracker_serializer.is_valid():
                claims_tracker_serializer.save()
            else:
                return Response(claims_tracker_serializer.errors, status=400)
        return Response(claims_tracker_serializer.data)
    if request.method == "PUT":
        data = JSONParser().parse(request)
        claims_tracker_serializer = ClaimsTrackerSerializer(claims_tracker, data=data)
        if claims_tracker_serializer.is_valid():
            claims_tracker_serializer.save()
            return Response(claims_tracker_serializer.data)
        return Response(claims_tracker_serializer.errors, status=400)
