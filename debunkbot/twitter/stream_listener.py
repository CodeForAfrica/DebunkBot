import json
import logging
from typing import List, Optional

from tweepy import Stream
from tweepy.streaming import StreamListener

from debunkbot.tasks import process_tweet
from debunkbot.twitter.api import create_connection

logger = logging.getLogger(__name__)


class Listener(StreamListener):
    """Tweepy Stream Listener Wrapper"""

    def __init__(self):
        super(Listener, self).__init__()
        self.__api = create_connection()
        self.twitter_stream = None

    def on_data(self, data) -> bool:
        """
        Processes and store the stream data in the member variable as soon
        as data is available
        """
        data = json.loads(data)
        if data:
            entities = data.get("entities")
            if entities:
                debunked_urls = entities.get("urls")
                if debunked_urls:
                    shared_info = [
                        url.get("expanded_url") for url in debunked_urls if url
                    ]
                else:
                    shared_info = data.get("text")
                if type(shared_info) == list:
                    """
                    Since a tweet might contain more than one URl,
                    We should check all of them.
                    """
                    for url in shared_info:
                        process_tweet.delay(url, data)
                else:
                    process_tweet.delay(shared_info, data)
            else:
                logger.error(data)
        return True

    def on_error(self, status: int) -> Optional[bool]:
        logger.error("Error occured ", status)
        """
        Stops the stream once API rate limit has been reached
        """
        if status == 420:
            if self.twitter_stream:
                self.twitter_stream.disconnect()
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
