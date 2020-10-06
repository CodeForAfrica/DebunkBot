from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from debunkbot.models import ClaimsDatabase

from .factories import ClaimsTrackerFactory, SuperUserFactory


class TestClaimsTracker(TestCase):
    @classmethod
    def setUpTestData(cls):
        ClaimsTrackerFactory.create()
        SuperUserFactory.create()

    def setUp(self):
        self.client = APIClient()
        self.claim_db = ClaimsDatabase.objects.first()
        # Get current user token
        self.token = Token.objects.first().key

    def test_claims_tracker_endpoint_requires_authentication(self):
        response = self.client.get("/claims_tracker/1/")
        self.assertEqual(401, response.status_code)

    def test_claims_tracker_endpoint_returns_tracking_info(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(f"/claims_tracker/{self.claim_db.id}/")
        # Stop including any credentials for the other tests
        self.client.credentials()
        expected_response = {
            "total_claims": 0,
            "current_offset": 0,
            "claim_db": self.claim_db.id,
        }
        self.assertEqual(expected_response, response.json())

    def test_updating_tracking_info_works(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        data = {"total_claims": 100, "current_offset": 10, "claim_db": self.claim_db.id}
        response = self.client.put(
            f"/claims_tracker/{self.claim_db.id}/", data=data, format="json"
        )
        self.assertEqual(200, response.status_code)
        get_request = self.client.get(f"/claims_tracker/{self.claim_db.id}/")
        # Stop including any credentials for the other tests
        self.client.credentials()
        self.assertEqual(data, get_request.json())
