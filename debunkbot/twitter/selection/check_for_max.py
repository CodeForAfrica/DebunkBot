from datetime import datetime
from typing import List, Optional

from debunkbot.models import Tweet


def check_for_max(tweets: List[dict]) -> Optional[Tweet]:
    max_tweet = max(tweets, key=lambda x: x.tweet['weight'])  # type: dict
    max_tweets = [tweet for tweet in tweets if tweet.tweet['weight'] == max_tweet.tweet['weight']]  # type: list
    if len(max_tweets) == 0:
        return None
    else:
        return sorted(max_tweets, key=lambda x: datetime.strptime(x.tweet['created_at'], "%a %b %d %H:%M:%S %z %Y"))[0]
