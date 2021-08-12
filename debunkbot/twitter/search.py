import random

from debunkbot.models import Claim


def start_claims_search():
    # pick a random number of claims
    total_claims = Claim.objects.count()
    start = random.randint(0, total_claims)
    claims = Claim.objects.values("claim_first_appearance")[start : start + 100]

    from debunkbot.tasks import search_single_claim

    for claim in claims:
        claim = claim["claim_first_appearance"]
        search_single_claim.delay(claim)


def search_claim_url(url, api):
    match = api.search(url)
    if match:
        tweet = match[0]._json
        return tweet
