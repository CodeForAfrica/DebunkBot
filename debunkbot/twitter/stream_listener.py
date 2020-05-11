import json
import os
from typing import Optional, List

from tweepy import Stream
from tweepy.streaming import StreamListener

from debunkbot.models import Tweet
from utils.twitter.connection import create_connection


class Listener(StreamListener):
    """Tweepy Stream Listener Wrapper"""

    def __init__(self):
        super(Listener, self).__init__()
        self.__api = create_connection()

    def on_data(self, data) -> bool:
        """
        Processes and store the stream data in the member variable as soon
        as data is available
        """
        data = json.loads(data)
        Tweet.objects.create(tweet=data)
        return True

    def on_error(self, status: int) -> Optional[bool]:
        """
        Stops the stream once API rate limit has been reached
        """
        print('error', flush=True, end=', ')
        print(status, flush=True)
        if status == 420:
            return False

    def listen(self, track_list: List[str]) -> None:
        """
        Starts the listening process
        """
        print(track_list, flush=True)
        twitter_stream = Stream(self.__api.auth, Listener())  # type: Stream
        twitter_stream.filter(track=track_list)


def stream(track_list: List[str]) -> None:
    """
    Initializes the listener class and runs the listen method
    """
    Listener().listen(track_list)
