from django.test import TestCase
from test.support import EnvironmentVarGuard

from utils.twitter.stream_listener import Listener


class TestTweeterStream(TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.clear()
    
    def test_keys_required_for_twitter_authorization_are_provided(self):
        """
            Test to ensure that keys required for twitter authoization i.e
            CLIENT_KEY, CLIENT_SECRET, ACCESS_TOKEN and ACCESS_SECRET
            are always set in the environment variables 
            while creating a StreamListener.
        """
        with self.assertRaises(Exception):
            Listener()
