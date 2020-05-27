from datetime import datetime
from typing import List, Optional

from django.conf import settings

from debunkbot.models import Tweet


def check_for_max(tweets: List[Tweet]) -> Optional[Tweet]:
    """Runs all related tweets through out little algorithm
    to determine which to select as the tweet we'll respond to
    """
    # The line below maps through our tweets retaining only those that
    # the accounts that tweeted them are not in our ignore list
    tweets_ = []  # type: List[Tweet]
    for tweet in tweets:
        if tweet.tweet['user']['screen_name'] not in settings.DEBUNKBOT_TWITTER_ACCOUNT_IGNORE_LIST:
            tweets_.append(tweet)

    max_tweet = max(tweets_, key=lambda x: x.tweet['weight'])  # type: Tweet
    max_tweets = [tweet for tweet in tweets_ if tweet.tweet['weight'] == max_tweet.tweet['weight']]  # type: List[Tweet]
    if len(max_tweets) == 0:
        return None
    else:
        return sorted(max_tweets, key=lambda x: datetime.strptime(x.tweet['created_at'], "%a %b %d %H:%M:%S %z %Y"))[0]
