from django.conf import settings
from django.db.models import Q

from debunkbot.models import ClaimsDatabase, DatabasePriority


def get_claims_to_search():
    claims = []
    database_priority = DatabasePriority.objects.filter(active=True).first()

    # Initialize db by priority level
    db_by_priority = {}
    priority_levels = ["low", "normal", "high"]
    for level in priority_levels:
        db_by_priority[level] = {
            "has_claims": ClaimsDatabase.objects.filter(
                deleted=False, priority=level
            ).exists(),
            "database_count": ClaimsDatabase.objects.filter(
                deleted=False, priority=level
            ).count(),
            "priority": getattr(database_priority, level),
        }

    # compute count for db by level
    for level in priority_levels:
        if db_by_priority[level]["has_claims"]:
            priority = db_by_priority[level]["priority"]
            total_free_priorities = 0
            total_priorities = 100
            computed_priority = priority
            for other_level in priority_levels:
                if other_level != level:
                    if not db_by_priority[other_level]["has_claims"]:
                        total_free_priorities += db_by_priority[other_level]["priority"]
                        total_priorities -= db_by_priority[other_level]["priority"]

            computed_priority += total_free_priorities * priority / total_priorities

            db_by_priority[level]["count"] = int(
                (computed_priority * settings.TWITTER_SEARCH_LIMIT / 100)
                / db_by_priority[level]["database_count"]
            )
        else:
            db_by_priority[level]["count"] = 0

    priority_databases = {
        "low": ClaimsDatabase.objects.filter(deleted=False, priority="low"),
        "normal": ClaimsDatabase.objects.filter(deleted=False, priority="normal"),
        "high": ClaimsDatabase.objects.filter(deleted=False, priority="high"),
    }

    for priority in db_by_priority:
        if db_by_priority[priority]["count"]:
            databases = priority_databases[priority]
            for database in databases:
                claims.extend(
                    database.claims.filter(
                        Q(processed=False)
                        and Q(rating=False)
                        and (
                            ~Q(claim_first_appearance="") or ~Q(claim_appearances=None)
                        )
                    ).values("claim_first_appearance", "claim_appearances",)[
                        : db_by_priority[priority]["count"]
                    ]
                )

    return claims


def start_claims_search():
    claims = get_claims_to_search()

    from debunkbot.tasks import search_single_claim

    for claim in claims:
        appearance = (
            claim.get("claim_first_appearance") or claim.get("claim_appearances")[0]
        )
        if appearance:
            search_single_claim.delay(appearance)


def search_claim_url(url, api):
    match = api.search(url)
    if match:
        tweet = match[0]._json
        if tweet.get("retweeted_status"):
            tweet = tweet["retweeted_status"]
        return tweet
