from django.conf import settings

from debunkbot.models import ClaimsDatabase, DatabasePriority


def get_claims_to_search():
    claims = []
    database_priority = DatabasePriority.objects.first()

    low_priority_claims_databases = ClaimsDatabase.objects.filter(
        deleted=False, priority="low"
    )
    normal_priority_claims_databases = ClaimsDatabase.objects.filter(
        deleted=False, priority="normal"
    )
    high_priority_claims_databases = ClaimsDatabase.objects.filter(
        deleted=False, priority="high"
    )

    low_priority_count = normal_priority_count = high_priority_count = 0
    if low_priority_claims_databases.count() == 0:
        if normal_priority_claims_databases.count() > 0:
            normal_priority_count += int(
                database_priority.normal
                / (database_priority.normal + database_priority.high)
                * database_priority.low
            )
        if high_priority_claims_databases.count() > 0:
            high_priority_count += int(
                database_priority.high
                / (database_priority.normal + database_priority.high)
                * database_priority.low
            )

    if normal_priority_claims_databases.count() == 0:
        if low_priority_claims_databases.count() > 0:
            low_priority_count += int(
                database_priority.low
                / (database_priority.low + database_priority.high)
                * database_priority.normal
            )
        if high_priority_claims_databases.count() > 0:
            high_priority_count += int(
                database_priority.high
                / (database_priority.low + database_priority.high)
                * database_priority.normal
            )

    if high_priority_claims_databases.count() == 0:
        if low_priority_claims_databases.count() > 0:
            low_priority_count += int(
                database_priority.low
                / (database_priority.low + database_priority.high)
                * database_priority.normal
            )
        if normal_priority_claims_databases.count() > 0:
            normal_priority_count += int(
                database_priority.normal
                / (database_priority.normal + database_priority.high)
                * database_priority.high
            )

    if low_priority_count:
        low_priority_count = (
            low_priority_count // low_priority_claims_databases.count()
        ) * settings.DEBUNKBOT_SEARCHEABLE_CLAIMS_COUNT
        for claim_database in low_priority_claims_databases:
            claims.append(
                claim_database.claims.filter(processed=False, rating=False).values(
                    "claim_first_appearance"
                )[:low_priority_count]
            )
    if normal_priority_count:
        normal_priority_count = (
            normal_priority_count // normal_priority_claims_databases.count()
        ) * settings.DEBUNKBOT_SEARCHEABLE_CLAIMS_COUNT
        for claim_database in normal_priority_claims_databases:
            claims.append(
                claim_database.claims.filter(processed=False, rating=False).values(
                    "claim_first_appearance"
                )[:normal_priority_count]
            )

    if high_priority_count:
        high_priority_count = (
            high_priority_count // high_priority_claims_databases.count()
        ) * settings.DEBUNKBOT_SEARCHEABLE_CLAIMS_COUNT
        for claim_database in high_priority_claims_databases:
            claims.append(
                claim_database.claims.filter(processed=False, rating=False).values(
                    "claim_first_appearance"
                )[:high_priority_count]
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
