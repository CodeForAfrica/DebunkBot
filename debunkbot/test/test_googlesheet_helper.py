from django.test import TestCase

from debunkbot.models import GoogleSheetCredentials, MessageTemplate
from debunkbot.twitter.selection.check_for_max import get_ignore_list
from debunkbot.utils.gsheet.helper import GoogleSheetHelper

from .factories import (
    GoogleSheetCredentialsFactory,
    GSheetClaimsDatabaseFactory,
    IgnoreListGsheetFactory,
)


class TestGoogleSheetHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        GSheetClaimsDatabaseFactory.create()
        GoogleSheetCredentialsFactory.create()

    def test_lack_of_google_credentials_raises_exception(self):
        GoogleSheetCredentials.objects.all().delete()
        with self.assertRaises(Exception):
            GoogleSheetHelper()

    def test_fetch_response_messages_functionality(self):
        """
            Test the google sheet helper is able to fetch response messages from the googlesheet
        """
        self.assertEqual(0, MessageTemplate.objects.count())

        google_sheet_helper = GoogleSheetHelper()
        google_sheet_helper.fetch_response_messages()
        self.assertEqual(2, MessageTemplate.objects.count())

    def test_fetch_ignore_list_functionality(self):
        # Before adding an ignore list the get_ignore_list should return an empty list.
        self.assertEqual(0, len(get_ignore_list()))
        IgnoreListGsheetFactory.create()
        self.assertEqual(2, len(get_ignore_list()))
