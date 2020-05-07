from unittest import TestCase
from test.support import EnvironmentVarGuard

from utils.gsheet.helper import GoogleSheetHelper
class TestGsheetHelper(TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.unset('GOOGLE_CREDENTIALS')
        
    def test_google_credentials_required(self):
        """
            Test to ensure that GOOGLE_CREDENTIALS are always set in the environment variables 
            while creating a GoogleSheetHelper.
        """
        with self.assertRaises(Exception):
            GoogleSheetHelper()
    
    def test_google_credentials_provided_has_required_values(self):
        """
            Test to ensure the GOOGLE_CREDENTIALS provided has required values e.g
            sheet_name
        """
        self.env.set('GOOGLE_CREDENTIALS', "{}")
        with self.assertRaises(Exception):
            GoogleSheetHelper()

        self.env.set('GOOGLE_CREDENTIALS', "{'sheet_name': '[DUMMY] Fact Check'}")
