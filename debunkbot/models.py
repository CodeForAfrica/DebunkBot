from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from debunkbot.manager import GSheetClaimsDatabaseQuerySet

RESPONSE_MODES = (
    ("No Responses", "Send No Response"),
    ("Response List", "Use a Response List"),
    ("Open Response", "Send Responses to any twitter account"),
)


class Tweet(models.Model):
    tweet = JSONField()
    responded = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    deleted = models.BooleanField(
        default=False, help_text="Has this tweet been deleted by the author?"
    )
    claim = models.ForeignKey(
        "Claim", related_name="tweets", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.tweet.get("text")

    class Meta:
        db_table = "tweets"


class Reply(models.Model):
    """
    Class for holding our reply to a tweet
    """

    reply = models.TextField(help_text="The reply that we sent.")
    reply_id = models.CharField(
        max_length=255,
        help_text="The Id of our reply. We use this to track impact of our reply",
    )
    # We store the Reply author since we require it while finding the impact of this reply.
    # In case we have new tweeter credentials for the bot,
    # having stored the reply_author will ensure we know what to track.
    reply_author = models.CharField(
        max_length=255,
        help_text="The Twitter handle of the account that sent the reply",
    )
    tweet = models.OneToOneField("Tweet", on_delete=models.SET_NULL, null=True)
    "Everything we receive from twitter concerning our reply"
    data = JSONField()

    def __str__(self):
        return self.reply_id


class Impact(models.Model):
    """
    Class for holding the impact of our reply.
    """

    reply = models.OneToOneField("Reply", on_delete=models.SET_NULL, null=True)
    likes_count = models.IntegerField(
        help_text="Number of people who have liked our reply."
    )
    replies_count = models.IntegerField(
        help_text="Number of replies we have received on our reply."
    )
    retweet_count = models.IntegerField(
        help_text="Number of times our reply has been retweeted."
    )
    replies = models.TextField(help_text="All replies we have received on our reply.")
    "Everything we receive from twitter concerning our reply impact"
    data = JSONField()
    tweet_deleted = models.BooleanField(
        default=False, help_text="Has the tweet we replied to been deleted?"
    )

    def __str__(self):
        return f"Impact {self.likes_count} Likes, {self.replies_count} Replies"


class Claim(models.Model):
    fact_checked_url = models.TextField(
        help_text="The URL to the debunked claim.", blank=True, null=True
    )
    claim_reviewed = models.TextField(help_text="The claim that has been debunked.")
    claim_date = models.CharField(
        max_length=255,
        help_text="The date when the claim was made.",
        blank=True,
        null=True,
    )
    claim_location = models.CharField(
        max_length=255,
        help_text="The location where the claim was made.",
        blank=True,
        null=True,
    )
    claim_first_appearance = models.TextField(
        blank=True, null=True, help_text="Link to where the claim first appeared."
    )
    claim_appearances = ArrayField(
        models.TextField(),
        null=True,
        help_text="Links to where the claims appeared, comma separated.",
    )
    claim_phrase = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Claim phrase that we should track.",
    )
    claim_author = models.CharField(
        max_length=255, blank=True, null=True, help_text="The author of the claim"
    )
    claim_db = models.ForeignKey(
        "ClaimsDatabase", related_name="claims", on_delete=models.CASCADE, null=True,
    )
    rating = models.BooleanField(default=False, help_text="Is the claim true or false?")
    processed = models.BooleanField(
        default=False,
        help_text="Determines if we've processed tweets related to this claim or not",
    )
    category = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="The category to which this claim belongs to.",
        default="MISINFO",
    )

    def __str__(self):
        return self.claim_reviewed or ""


class MessageTemplate(models.Model):
    message_template = models.CharField(
        max_length=255, help_text="Message template to use for sending reply"
    )
    message_template_source = models.ForeignKey(
        "MessageTemplateSource",
        related_name="message_templates",
        on_delete=models.CASCADE,
        null=True,
        help_text="The source of the message templates.",
    )
    message_template_category = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Category that this message template belongs to.",
    )

    def __str__(self):
        return self.message_template


class MessageTemplateSource(models.Model):
    key = models.CharField(
        max_length=255,
        help_text="The spreadsheet id from which we will be pulling message templates from.",
    )
    worksheet = models.CharField(
        max_length=255,
        help_text="The worksheet name from which the message templates will be fetched.",
    )
    column = models.CharField(
        max_length=255, help_text="The column holding the message templates."
    )

    def __str__(self):
        return f"{self.worksheet} - {self.key}"


class ClaimsDatabase(models.Model):
    name = models.CharField(
        unique=True, max_length=255, help_text="The name of the claims database",
    )
    deleted = models.BooleanField(
        help_text="Mark this claims database as deleted.", default=False
    )

    def __str__(self):
        return self.name


class GSheetClaimsDatabase(ClaimsDatabase):
    objects = GSheetClaimsDatabaseQuerySet.as_manager()
    key = models.CharField(
        max_length=255,
        help_text="The spreadsheet id for the database we're pulling from",
    )
    worksheets = ArrayField(
        models.CharField(max_length=255),
        help_text="List of workspaces to fetch data from, comma separated",
    )
    claim_url_column_names = ArrayField(
        models.CharField(max_length=255),
        help_text="List of columns to fetch claim urls from in this specific spreadsheet, comma separated",
    )
    claim_first_appearance_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim first appearance from in this specific spreadsheet",
        blank=True,
        null=True,
    )
    claim_phrase_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim phrases from in this specific spreadsheet",
        blank=True,
        null=True,
    )
    claim_rating_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim rating from in this specific spreadsheet",
    )
    claim_description_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim checked from in this specific spreadsheet",
    )
    claim_debunk_url_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim debunked from in this specific spreadsheet",
        blank=True,
        null=True,
    )
    claim_location_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim location from in this specific spreadsheet",
        blank=True,
        null=True,
    )
    claim_author_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim author from in this specific spreadsheet",
        blank=True,
        null=True,
    )
    claim_category_column_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The colum that contains claim category.",
    )
    message_template_source = models.ForeignKey(
        "MessageTemplateSource",
        related_name="claims_databases",
        on_delete=models.PROTECT,
        null=True,
        help_text="The message template source for this database.",
    )

    class Meta:
        verbose_name = "GoogleSheetClaimsDatabase"


class WebsiteClaimDatabase(ClaimsDatabase):
    url = models.URLField()


class GoogleSheetCredentials(models.Model):
    credentials = JSONField(
        help_text="The service account key needed by the application to access Google Sheet data."
    )

    def __str__(self):
        return self.credentials.get("client_email")

    class Meta:
        verbose_name_plural = "Google Sheet Credentials"


class BaseSheet(models.Model):
    key = models.CharField(max_length=255, help_text="")
    worksheet_name = models.CharField(max_length=255, help_text="")
    column_name = models.CharField(max_length=255, help_text="")

    def __str__(self):
        return self.key

    class Meta:
        abstract = True


class IgnoreListGsheet(BaseSheet):
    pass


class RespondListGsheet(BaseSheet):
    pass


class ResponseMode(models.Model):
    response_mode = models.CharField(
        help_text="Current response mode",
        choices=RESPONSE_MODES,
        verbose_name="Which response mode do you want to use?",
        default="No Responses",
        max_length=255,
    )

    def __str__(self):
        return self.response_mode


# Signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
