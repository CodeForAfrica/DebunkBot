import json
from typing import Optional, List

from tweepy import Stream
from tweepy.streaming import StreamListener

from debunkbot.models import Tweet
from debunkbot.twitter.api import create_connection

from utils.gsheet.helper import GoogleSheetHelper


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
        # Check if data.txt is in self.google_sheet
        tweet = Tweet.objects.create(tweet=data)
        debunked_urls = data.get('entities').get('urls')
        debunked_url = [url.get('expanded_url') for url in debunked_urls]
        
        sheet_data = self.google_sheet.cache_or_load_sheet()
        for row in sheet_data:
            if row.get('Claim First Appearance') in debunked_url:
                # This tweets belongs to this row
                tweet.sheet_row = row.get('row')
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
        twitter_stream.filter(track=track_list)


def stream(track_list: List[str]) -> None:
    """
    Initializes the listener class and runs the listen method
    """
    Listener().listen(track_list)
