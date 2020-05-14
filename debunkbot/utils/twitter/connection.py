import os

from tweepy import OAuthHandler, API


# Moved twitter's connection here so that we can reuse it across multiple twitter classes
def create_connection():
    auth = OAuthHandler(os.getenv('CLIENT_KEY'), os.getenv('CLIENT_SECRET'))  # type: OAuthHandler
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    api = API(
            auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)  # set wait limit on tweepy so we don't get blocked by Twitter
    return api
