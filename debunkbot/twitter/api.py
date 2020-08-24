import logging

import tweepy
from django.conf import settings
from tweepy import API, OAuthHandler

logger = logging.getLogger(__name__)


# Moved twitter's connection here so that we can reuse it across multiple twitter classes
def create_connection():
    auth = OAuthHandler(
        settings.TWITTER_CLIENT_KEY, settings.TWITTER_CLIENT_SECRET
    )  # type: OAuthHandler
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_SECRET)
    return API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    )  # set wait limit on tweepy so we don't get blocked by Twitter


def get_tweet_status(api, tweet_id):
    try:
        # Check if the tweet has been deleted.
        tweet_status = api.get_status(tweet_id)
    except tweepy.TweepError as error:
        if hasattr(error, "response"):
            if error.response.status_code == 404:
                # Tweet has been deleted by the author.
                logger.info(f"Tweet {tweet_id} Deleted")
                tweet_status = None
        logger.error("Error: ", error)
        return
    return tweet_status
