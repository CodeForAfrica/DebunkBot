from tweepy import OAuthHandler, API
from django.conf import settings


# Moved twitter's connection here so that we can reuse it across multiple twitter classes
def create_connection():
    auth = OAuthHandler(
        getattr(settings, 'TWITTER_CLIENT_KEY'),
        getattr(settings, 'TWITTER_CLIENT_SECRET'))  # type: OAuthHandler
    auth.set_access_token(
        getattr(settings, 'TWITTER_ACCESS_TOKEN'),
        getattr(settings, 'TWITTER_ACCESS_SECRET'))
    api = API(
            auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)  # set wait limit on tweepy so we don't get blocked by Twitter
    return api
