from django.test import TestCase
from django.core.cache import cache

from debunkbot.models import (Claim, )
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet, retrieve_claims_from_db

from .factories import GoogleSheetCredentialsFactory, GSheetClaimsDatabaseFactory, ClaimsFactory

class TestClaimsHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleSheetCredentialsFactory.create()
        GSheetClaimsDatabaseFactory.create()

    def test_fetch_claims_from_gsheet(self):
        total_claims = fetch_claims_from_gsheet()
        self.assertGreater(total_claims, 0)
    
    def test_retrieve_claims_from_db(self):
        """
        Test claims are saved into the database and cached to reduce access time.
        """
        claims_from_db = retrieve_claims_from_db()
        self.assertEqual(0, len(claims_from_db))

        # get claims from the google sheet and save them to the database.
        fetch_claims_from_gsheet()
        claims_from_db = retrieve_claims_from_db()
        self.assertGreater(len(claims_from_db), 0)

        # Test claims get cached 
        self.assertIsNotNone(cache.get('claims'))
    
    def test_maximum_claims_retrieve(self):
        """
            Test to ensure we are currently only retrieving 390 claims for our stream listener.
        """
        [ClaimsFactory.create() for _ in range(400)]
        self.assertEqual(390, len(retrieve_claims_from_db()))
    
    def tearDown(self):
        cache.clear()
