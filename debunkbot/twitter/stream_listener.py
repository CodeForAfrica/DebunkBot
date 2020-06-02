import json
import time
from typing import Optional, List

import logging
from django.conf import settings
from tweepy import Stream
from tweepy.streaming import StreamListener

from debunkbot.models import Tweet
from debunkbot.twitter.api import create_connection

from debunkbot.utils.gsheet.helper import GoogleSheetHelper


logger = logging.getLogger(__name__)


class Listener(StreamListener):
    """Tweepy Stream Listener Wrapper"""

    def __init__(self):
        super(Listener, self).__init__()
        self.__api = create_connection()
        self.google_sheet = GoogleSheetHelper()
        self.twitter_stream = None

    def on_data(self, data) -> bool:
        """
        Processes and store the stream data in the member variable as soon
        as data is available
        """
        data = json.loads(data)
        if data:
            debunked_urls = data.get('entities').get('urls')
            if debunked_urls:
                shared_info = [url.get('expanded_url') for url in debunked_urls if url]
            else:
                shared_info = data.get('text')
            claims = self.google_sheet.get_claims()
            for claim in claims:
                if (claim.claim_first_appearance or claim.claim_phrase) in shared_info:
                    # This tweets belongs to this claim
                    tweet = Tweet.objects.create(tweet=data)
                    tweet.claim = claim
                    value = self.google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_CLAIM_APPEARANCES_COLUMN)) + ', https://twitter.com/' + \
                            tweet.tweet['user']['screen_name'] + '/status/' + tweet.tweet['id_str']
                    profiles = self.google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_CLAIM_SENDER_COLUMN)) + str(tweet.tweet['user'])
                    # Update google sheet to reflect this claim appearance
                    self.google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_CLAIM_APPEARANCES_COLUMN), value)
                    self.google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_CLAIM_SENDER_COLUMN), profiles)
                    tweet.save()
        return True

    def on_error(self, status: int) -> Optional[bool]:
        logger.error("Error occured ", status)
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
        self.twitter_stream = twitter_stream


listener = Listener()

def stream(track_list: List[str]) -> None:
    """
    Initializes the listener class and runs the listen method
    """
    if listener.twitter_stream:
        logger.info("Disconnecting...")
        listener.twitter_stream.disconnect()
    
    listener.listen(track_list[:390])

