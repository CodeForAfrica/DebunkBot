from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

from debunkbot.manager import GSheetClaimsDatabaseManager


class Tweet(models.Model):
    tweet = JSONField()
    responded = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False, help_text="Has this tweet been deleted by the author?")
    claim = models.ForeignKey('Claim', related_name='tweets', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.tweet.get('text')

    class Meta:
        db_table = 'tweets'


class Reply(models.Model):
    """
    Class for holding our reply to a tweet
    """
    reply = models.TextField(help_text="The reply that we sent.")
    reply_id = models.CharField(
        max_length=255,
        help_text="The Id of our reply. We use this to track impact of our reply")
    # We store the Reply author since we require it while finding the impact of this reply.
    # In case we have new tweeter credentials for the bot,
    # having stored the reply_author will ensure we know what to track.
    reply_author = models.CharField(max_length=255, help_text="The twitter handle of the account that sent the reply")
    tweet = models.OneToOneField('Tweet', on_delete=models.SET_NULL, null=True)
    "Everything we receive from twitter concerning our reply"
    data = JSONField()

    def __str__(self):
        return self.reply_id


class Impact(models.Model):
    """
    Class for holding the impact of our reply.
    """
    reply = models.OneToOneField('Reply', on_delete=models.SET_NULL, null=True)
    likes_count = models.IntegerField(help_text="Number of people who have liked our reply.")
    replies_count = models.IntegerField(help_text="Number of replies we have received on our reply.")
    retweet_count = models.IntegerField(help_text="Number of times our reply has been retweeted.")
    replies = models.TextField(help_text="All replies we have received on our reply.")
    "Everything we receive from twitter concerning our reply impact"
    data = JSONField()
    tweet_deleted = models.BooleanField(default=False, help_text="Has the tweet we replied to been deleted?")

    def __str__(self):
        return f"Impact {self.likes_count} Likes, {self.replies_count} Replies"


class Claim(models.Model):
    fact_checked_url = models.TextField(help_text="The URL to the debunked claim.")
    claim_reviewed = models.TextField(help_text="The claim that has been debunked.")
    claim_date = models.CharField(max_length=255, help_text="The date when the claim was made.")
    claim_location = models.CharField(max_length=255, help_text="The location where the claim was made.")
    claim_first_appearance = models.TextField(null=True, help_text="Link to where the claim first appeared.")
    claim_appearances = ArrayField(
        models.TextField(), null=True, help_text="Links to where the claims appeared, separated by commas.")
    claim_phrase = models.CharField(max_length=255, null=True, help_text="Claim phrase that we should track.")
    claim_author = models.CharField(max_length=255, help_text="The author of the claim")
    claim_db = models.ForeignKey('GSheetClaimsDatabase', related_name='claims', on_delete=models.CASCADE, null=True)    
    rating = models.BooleanField(default=False, help_text="Is the claim true or false?")
    processed = models.BooleanField(
        default=False,
        help_text="Determines if we've processed tweets related to this claim or not")

    def __str__(self):
        return self.claim_reviewed or ''


class MessageTemplate(models.Model):
    message_template = models.CharField(max_length=255, help_text="Message template to use for sending reply")
    message_template_source = models.ForeignKey('MessageTemplateSource', related_name='message_templates', 
        on_delete=models.CASCADE, null=True, help_text="The source of the message templates.")

    def __str__(self):
        return self.message_template


class MessageTemplateSource(models.Model):
    key = models.CharField(
        max_length=255,
        help_text="The spreadsheet id from which we will be pulling message templates from.")
    worksheet = models.CharField(
        max_length=255,
        help_text="The worksheet name from which the message templates will be fetched.")
    column = models.CharField(
        max_length=255,
        help_text="The column holding the message templates.")
    
    def __str__(self):
        return f'{self.worksheet} - {self.key}'


class GSheetClaimsDatabase(models.Model):
    objects = GSheetClaimsDatabaseManager.as_manager()
    key = models.CharField(
        max_length=255,
        help_text="The spreadsheet id for the database we're pulling from")
    worksheets = ArrayField(
        models.CharField(max_length=255),
        help_text="List of workspaces to fetch data from; separated by commas")
    claim_url_column_names = ArrayField(
        models.CharField(max_length=255),
        help_text="List of columns to fetch claim urls from in this specific spreadsheet; separated by commas")
    claim_first_appearance_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim first appearance from in this specific spreadsheet",
        blank=True,
        null=True
        )
    claim_phrase_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim phrases from in this specific spreadsheet",
        blank=True,
        null=True
        )
    claim_rating_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim rating from in this specific spreadsheet")
    claim_description_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim checked from in this specific spreadsheet")
    claim_debunk_url_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim debunked from in this specific spreadsheet",
        blank=True,
        null=True
        )
    claim_location_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim location from in this specific spreadsheet",
        blank=True,
        null=True
        )
    claim_author_column_name = models.CharField(
        max_length=255,
        help_text="The column to fetch claim author from in this specific spreadsheet",
        blank=True,
        null=True
        )
    claim_db_name = models.CharField(
        unique=True,
        max_length=255,
        help_text="The name of the sheet storing the recorded claims.")
    message_template_source = models.ForeignKey('MessageTemplateSource', related_name='claims_databases', 
        on_delete=models.PROTECT, null=True, help_text="The message template source for this database.")
    deleted = models.BooleanField(help_text="Mark this claims database as deleted instead of removing it from the database.",
        default=False)
    
    class Meta:
        verbose_name = "GoogleSheetClaimsDatabase"

    def __str__(self):
        return self.claim_db_name

class GoogleSheetCredentials(models.Model):
    credentials =  JSONField(help_text="The API key needed by the application to access Google Sheet data.")

    def __str__(self):
        return self.credentials.get('client_email')


class IgnoreListGsheet(models.Model):
    key = models.CharField(max_length=255, help_text="The key of the google sheet holding the ignore list.")
    worksheet_name = models.CharField(max_length=255, help_text="The name of the workspace containing the ignore list")
    column_name = models.CharField(max_length=255, help_text="The column name containing the ignore list.")

    def __str__(self):
        return self.key
