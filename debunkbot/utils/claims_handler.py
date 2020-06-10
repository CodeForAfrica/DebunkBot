from typing import Optional, List

from django.conf import settings
from django.core.cache import cache

from debunkbot.models import GSheetClaimsDatabase, Claim
from debunkbot.utils.gsheet.helper import GoogleSheetHelper


def retrieve_claims_from_db() -> Optional[List[dict]]:
    """
    Instance method that loads the claims either from the
    cache or from the database depending on whether
    we have a saved version in our cache or not
    :return: Claims
    """
    claims = cache.get('claims')
    if not claims:
        claims = Claim.objects.all()
        cache.set('claims', claims, timeout=int(settings.DEBUNKBOT_CACHE_TTL))
    return claims


def fetch_claims_from_gsheet():
    claim_databases = GSheetClaimsDatabase.objects.all()
    google_sheet_helper = GoogleSheetHelper()
    total_claims = 0
    for claim_database in claim_databases:
        sheet = google_sheet_helper.get_sheet(claim_database.key)
        for worksheet_name in claim_database.worksheets:
            worksheet = sheet.worksheet(worksheet_name)
            all_records = worksheet.get_all_records()
            for record in all_records:
                claim_rating = record.get(claim_database.claim_rating_column_name)
                if claim_rating:
                    rating = claim_rating.upper()
                    if rating in ['TRUE', 'FALSE']:
                        record['rating'] = rating == 'TRUE'
                        get_or_create_claim(claim_database, record)
                        total_claims += 1
    return total_claims


def get_or_create_claim(claim_database, record):
    # gets a claim from the database or creates it if it doesn't exist.
    claim_first_appearance_column_name = claim_database.claim_first_appearance_column_name
    claim_first_appearance = record.get(claim_first_appearance_column_name)[:255]
    if claim_first_appearance:
        claim, created = Claim.objects.get_or_create(claim_first_appearance=claim_first_appearance)
    else:
        # If claim first appearance doesn't exist, use the first claim in the claim appearances as the first claim.
        claim_first_appearance = record.get(claim_database.claim_url_column_names[0])[:255]
        claim, created = Claim.objects.get_or_create(claim_first_appearance=claim_first_appearance)
    appearances = []
    for claim_appearance_column in claim_database.claim_url_column_names:
        appearances.append(record.get(claim_appearance_column))

    claim.claim_appearances = appearances
    claim.claim_reviewed = record.get(claim_database.claim_description_column_name)
    claim.claim_phrase = record.get(claim_database.claim_phrase_column_name)
    claim.claim_date = 'N/A'
    claim.claim_location = record.get(claim_database.claim_location_column_name) or 'N/A'
    claim.fact_checked_url = record.get(claim_database.claim_debunk_url_column_name) or 'N/A'
    claim.claim_author = record.get(claim_database.claim_author_column_name) or 'N/A'
    claim.claim_db = claim_database
    claim.rating = record.get('rating')
    claim.save()
    
    return claim
