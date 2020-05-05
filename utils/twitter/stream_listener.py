import os
from typing import Optional, List

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


class Listener(StreamListener):
    """Tweepy Stream Listener Wrapper"""

    def __init__(self):
        super(Listener, self).__init__()
        self.__auth = OAuthHandler(os.getenv('CLIENT_KEY'), os.getenv('CLIENT_SECRET'))  # type: OAuthHandler
        self.__auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
        self.__stream = []  # type: list

    @property
    def stream(self) -> list:
        """
        Retrieves stream data after it has been processed by on_data
        """
        return self.__stream

    def on_data(self, data: dict) -> bool:
        """
        Processes and store the stream data in the member variable as soon
        as data is available
        """
        self.__stream.append(data)
        print(self.__stream, flush=True)  # TODO: remove when we make use of the data
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
        twitter_stream = Stream(self.__auth, Listener())  # type: Stream
        twitter_stream.filter(track=track_list)


def stream(track_list: List[str]) -> None:
    """
    Initializes the listener class and runs the listen method
    """
    Listener().listen(track_list)
