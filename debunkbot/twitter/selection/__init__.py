from typing import List, Optional

from ...models import Claim, Tweet
from .check_for_max import check_for_max


def selector() -> Optional[Tweet]:
    """Entry point to our selection algorithm. Selects a claim
    from the database which we haven't processed. One that has
    unprocessed tweets assigned to it and returns the single
    tweet our selection algorithm returns
    """
    claims = Claim.objects.filter(processed=False)  # type: List[Claim]
    for claim in claims:
        tweets = Tweet.objects.filter(claim=claim, processed=False)  # type: List[Tweet]
        if len(tweets) > 0:
            return check_for_max(tweets)
