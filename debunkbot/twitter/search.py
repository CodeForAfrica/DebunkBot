from django.conf import settings

from debunkbot.models import ClaimsDatabase, DatabasePriority


def get_claims_to_search():
    claims = []
    database_priority = DatabasePriority.objects.filter(active=True).first()

    priority_databases = {
        "low": ClaimsDatabase.objects.filter(deleted=False, priority="low"),
        "normal": ClaimsDatabase.objects.filter(deleted=False, priority="normal"),
        "high": ClaimsDatabase.objects.filter(deleted=False, priority="high"),
    }

    priority_count = {
        "low": database_priority.low,
        "normal": database_priority.normal,
        "high": database_priority.high,
    }

    for priority in priority_count:
        """
        For the 3 priority levels, we want to redistribute a database priority \
            incase no claim database exists with the given priority.
        """
        if not priority_databases[priority].count():
            priority_count[priority] = 0
            if priority == "low":
                other_priority = {"normal": "high", "high": "normal"}
            if priority == "normal":
                other_priority = {"low": "high", "high": "low"}
            if priority == "high":
                other_priority = {"low": "normal", "normal": "low"}
            for other_priority_key in other_priority:
                # Incase one of the other databases is available, either
                # 1. Distribute the original database priority to the other \
                # databases based on each database priority
                # or 2. If the 3rd database type doesn't exist then allocate all \
                # the priorities of current database to it.
                if priority_databases[other_priority_key].count():
                    if priority_databases[other_priority[other_priority_key]]:
                        priority_count[other_priority_key] += int(
                            getattr(database_priority, other_priority_key)
                            / (
                                getattr(database_priority, other_priority_key)
                                + getattr(
                                    database_priority,
                                    other_priority[other_priority_key],
                                )
                            )
                            * getattr(database_priority, priority)
                        )
                    else:
                        priority_count[other_priority_key] += getattr(
                            database_priority, priority
                        )

    for priority in priority_count:
        if priority_count[priority]:
            priority_count[priority] = int(
                (
                    (priority_count[priority] / 100)
                    / priority_databases[priority].count()
                )
                * settings.DEBUNKBOT_SEARCHEABLE_CLAIMS_COUNT
            )

            for claim_database in priority_databases[priority]:
                claims.append(
                    claim_database.claims.filter(processed=False, rating=False).values(
                        "claim_first_appearance"
                    )[: priority_count[priority]]
                )

    return claims


def start_claims_search():
    claims = get_claims_to_search()

    from debunkbot.tasks import search_single_claim

    for claim in claims:
        claim = claim["claim_first_appearance"]
        search_single_claim.delay(claim)


def search_claim_url(url, api):
    match = api.search(url)
    if match:
        tweet = match[0]._json
        return tweet
