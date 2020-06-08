from debunkbot.models import SheetInformation
from debunkbot.utils.gsheet.helper import GoogleSheetHelper


def fetch_claims_from_gsheet():
    sheet_infos = SheetInformation.objects.all()
    google_sheet_helper = GoogleSheetHelper()
    claims = []
    for sheet_info in sheet_infos:
        sheet = google_sheet_helper.get_sheet(sheet_info.key)
        for worksheet_name in sheet_info.workspaces:
            worksheet = sheet.worksheet(worksheet_name)
            all_records = worksheet.get_all_records()
            for record in all_records:
                claim_rating = record.get(sheet_info.claim_rating_column)
                if claim_rating:
                    if claim_rating.upper() == 'TRUE':
                        record['rating'] = True
                    elif claim_rating.upper() == 'FALSE':
                        record['rating'] = False
                    else:
                        # Skip this record since we don't know if it is true or false
                        continue
                    claims.append(get_or_create_claim(sheet_info, record))
    return claims

def get_or_create_claim(sheet_info, record):
    # gets a claim from the database or creates it if it doesn't exist.
    column_name = sheet_info.claim_checked_column
    claim, created = Claim.objects.get_or_create(claim_reviewed=record.get(column_name)[:255])
    if created:
        claim.claim_first_appearance = record.get(sheet_info.claim_first_appearance) or 'N/A'
        claim.claim_phrase = record.get(sheet_info.claim_phrase) or 'N/A'
        claim.claim_date = 'N/A'
        claim.claim_location = 'N/A'
        claim.fact_checked_url = 'N/A'
        claim.claim_author = 'N/A'
        claim.rating = record.get('rating')
        claim.sheet_row = 'N/A'
        claim.save()
    
    return claim
