import os
import json
import factory

from debunkbot.models import (GSheetClaimsDatabase, 
                                GoogleSheetCredentials,
                                 Claim, IgnoreListGsheet, MessageTemplateSource)


class MessageTemplatesSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MessageTemplateSource
        django_get_or_create = ("key", )

    key = os.environ.get('DEBUNKBOT_TEST_GSHEET_SHEET_ID')
    worksheet = "Bot Responses"
    column = "Response Messages"

    
class GSheetClaimsDatabaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GSheetClaimsDatabase
        django_get_or_create = ("key", )
    
    key = os.environ.get('DEBUNKBOT_TEST_GSHEET_SHEET_ID')
    worksheets = ["Debunked Claims", ]
    claim_first_appearance_column_name = "Platform URL"
    claim_url_column_names = ["Platform URL", ]
    claim_rating_column_name = "Conclusion"
    claim_description_column_name = "Claim Checked"
    claim_debunk_url_column_name = "PesaCheck URL"
    claim_db_name = "Claim Database For Integration test"
    message_template_source = factory.SubFactory(MessageTemplatesSourceFactory)


class GoogleSheetCredentialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoogleSheetCredentials
        django_get_or_create = ("credentials", )
    
    credentials = json.loads(os.environ.get('DEBUNKBOT_TEST_GSHEET_SHEET_CREDENTIALS', {}))


class ClaimsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Claim
        django_get_or_create = ("claim_reviewed", )
    
    fact_checked_url = factory.Faker("url")
    claim_reviewed = factory.Faker("sentence")
    claim_date = factory.Faker("date")
    claim_location = factory.Faker("country")
    claim_first_appearance = factory.Faker("url")
    claim_phrase = factory.Faker("text")
    claim_author = factory.Faker("name")
    rating = False
    processed = factory.Faker("boolean")
    claim_db = factory.SubFactory(GSheetClaimsDatabaseFactory)


class IgnoreListGsheetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IgnoreListGsheet
        django_get_or_create = ("key", )
    
    key =  os.environ.get('DEBUNKBOT_TEST_GSHEET_SHEET_ID')
    worksheet_name = "Ignore List"
    column_name = "Accounts to ignore"
