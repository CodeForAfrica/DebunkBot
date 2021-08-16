from typing import Optional

from ...models import Tweet
from .check_for_max import check_for_max


def selector() -> Optional[Tweet]:
    """Entry point to our selection algorithm. Selects a claim
    from the database which we haven't processed. One that has
    unprocessed tweets assigned to it and returns the single
    tweet our selection algorithm returns
    """
    tweets = Tweet.objects.filter(processed=False)
    tweets_to_process = []
    for tweet in tweets:
        if not tweet.claim.processed:
            tweets_to_process.append(tweet)
    if len(tweets_to_process) > 0:
        return check_for_max(tweets_to_process)
    return None
