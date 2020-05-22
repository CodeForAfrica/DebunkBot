import tweepy
from tweepy import OAuthHandler, API
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

# Moved twitter's connection here so that we can reuse it across multiple twitter classes
def create_connection():
    auth = OAuthHandler(
        settings.TWITTER_CLIENT_KEY,
        settings.TWITTER_CLIENT_SECRET)  # type: OAuthHandler
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_SECRET)
    return API(
            auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)  # set wait limit on tweepy so we don't get blocked by Twitter

def get_tweet_status(api, tweet_id, tweet_in_db=None):
    try:
        # Check if the tweet has been deleted.
        tweet_status = api.get_status(tweet_id)
    except tweepy.TweepError as error:
        tweet_status = None
        if error.api_code == 144:
            # Tweet has been deleted by the author.
            logger.info(f"Tweet {tweet_id} Deleted")
            if tweet_in_db:
                tweet_in_db.deleted = True
                tweet_in_db.save()
    
    return tweet_status
