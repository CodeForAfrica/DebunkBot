from typing import Optional, List

from .check_for_max import check_for_max
from ...models import Claim, Tweet


def selector() -> Optional[Tweet]:
    claims = Claim.objects.filter(processed=False)  # type: List[Claim]
    for claim in claims:
        tweets = Tweet.objects.filter(claim=claim)  # type: List[Tweet]
        if len(tweets) > 0:
            return check_for_max(tweets)
