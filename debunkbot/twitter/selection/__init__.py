from typing import Union

from .check_for_max import check_for_max
from ...models import Claim, Tweet


def selector() -> Union[Tweet, None]:
    tweets = []
    claim = Claim.objects.filter(processed=False).last()
    if claim:
        tweets = Tweet.objects.filter(claim=claim)
    return check_for_max(tweets) if tweets else {}
