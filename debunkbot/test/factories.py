import json
import os

import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from debunkbot.models import (
    Claim,
    ClaimsTracker,
    GoogleSheetCredentials,
    GSheetClaimsDatabase,
    IgnoreListGsheet,
    MessageTemplateSource,
)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "credentials.json")) as _file:
    credentials = json.loads(_file.read())


class MessageTemplatesSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MessageTemplateSource
        django_get_or_create = ("spreadsheet_id",)

    spreadsheet_id = os.environ.get("DEBUNKBOT_TEST_GSHEET_SHEET_ID")
    worksheet = "Bot Responses"
    column = "Response Messages"


class GSheetClaimsDatabaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GSheetClaimsDatabase
        django_get_or_create = ("spreadsheet_id",)

    spreadsheet_id = os.environ.get("DEBUNKBOT_TEST_GSHEET_SHEET_ID")
    worksheets = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_SHEET_WORKSHEETS", "KENYA"
    ).split(",")
    claim_first_appearance_column_name = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_FIRST_APPEARANCE", "Platform URL"
    )
    claim_url_column_names = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_APPEARANCES", "Platform URL"
    ).split(",")
    claim_rating_column_name = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_RATING_COLUMN", "Debunk Rating"
    )
    claims_ratings = os.environ.get("DEBUNKBOT_TEST_GSHEET_RATINGS", "False.").split(
        ","
    )
    claims_start_row = 2
    claim_description_column_name = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_CLAIM_DESCRIPTION", "Claim Checked"
    )
    claim_debunk_url_column_name = os.environ.get(
        "DEBUNKBOT_TEST_GSHEET_DEBUNK_URL", "PesaCheck URL"
    )
    name = "Claim Database For Integration test"
    message_template_source = factory.SubFactory(MessageTemplatesSourceFactory)


class GoogleSheetCredentialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoogleSheetCredentials
        django_get_or_create = ("credentials",)

    credentials = credentials


class ClaimsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Claim
        django_get_or_create = ("claim_reviewed",)

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
        django_get_or_create = ("spreadsheet_id",)

    spreadsheet_id = os.environ.get("DEBUNKBOT_TEST_GSHEET_SHEET_ID")
    worksheet_name = "Ignore List"
    column_name = "Accounts to ignore"


class ClaimsTrackerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClaimsTracker

    claim_db = factory.SubFactory(GSheetClaimsDatabaseFactory)
    total_claims = 0
    current_offset = 0


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))
    is_staff = True
    is_superuser = True
