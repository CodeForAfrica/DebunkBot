import json
import time
from typing import Optional, List

from django.conf import settings
from tweepy import Stream
from tweepy.streaming import StreamListener

from debunkbot.models import Tweet
from debunkbot.twitter.api import create_connection

from debunkbot.utils.gsheet.helper import GoogleSheetHelper


class Listener(StreamListener):
    """Tweepy Stream Listener Wrapper"""

    def __init__(self):
        super(Listener, self).__init__()
        self.__api = create_connection()
        self.google_sheet = GoogleSheetHelper()

    def on_data(self, data) -> bool:
        """
        Processes and store the stream data in the member variable as soon
        as data is available
        """
        data = json.loads(data)
        # Update google sheet to reflect this claim appearance
        tweet = Tweet.objects.create(tweet=data)
        debunked_urls = data.get('entities').get('urls')
        debunked_url = [url.get('expanded_url') for url in debunked_urls]
        
        claims = self.google_sheet.get_claims()
        for claim in claims:
            if claim.claim_first_appearance in debunked_url:
                # This tweets belongs to this claim
                tweet.claim = claim
        value = self.google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.CLAIM_APPEARANCES_COLUMN)) + ', https://twitter.com/' + \
                tweet.tweet['user']['screen_name'] + '/status/' + tweet.tweet['id_str']
        print("Value is ", value)
        self.google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.CLAIM_APPEARANCES_COLUMN), value)

        tweet.save()
        return True

    def on_error(self, status: int) -> Optional[bool]:
        """
        Stops the stream once API rate limit has been reached
        """
        if status == 420:
            return False

    def listen(self, track_list: List[str]) -> None:
        """
        Starts the listening process
        """
        twitter_stream = Stream(self.__api.auth, Listener())  # type: Stream
        twitter_stream.filter(track=track_list, is_async=True)
        refresh_tracklist_timeout = int(settings.REFRESH_TRACK_LIST_TIMEOUT)
        time.sleep(refresh_tracklist_timeout)
        print("Disconnecting...")
        twitter_stream.disconnect()


def stream(track_list: List[str]) -> None:
    """
    Initializes the listener class and runs the listen method
    """
    Listener().listen(track_list)
