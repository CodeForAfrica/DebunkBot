from django.contrib.postgres.fields import JSONField
from django.db import models


class Tweet(models.Model):
    tweet = JSONField()
    responded = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False, help_text="Has this tweet been deleted by the author.")
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
    reply_author = models.CharField(max_length=255, help_text="The tweet handle of the account that sent the reply")
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
    retweet_count = models.IntegerField(help_text="Number of retweets our reply has been retweeted.")
    replies = models.TextField(help_text="All replies we have received on our reply.")
    "Everything we receive from twitter concerning our reply impact"
    data = JSONField()
    tweet_deleted = models.BooleanField(default=False, help_text="Has the tweet we replied to been deleted?")

    def __str__(self):
        return f"Impact {self.likes_count} Likes, {self.replies_count} Replies"


class Claim(models.Model):
    fact_checked_url = models.CharField(max_length=255, help_text="The URL to the debunked claim.")
    claim_reviewed = models.CharField(max_length=255, help_text="The claim that has been debunked.")
    claim_date = models.CharField(max_length=255, help_text="The date when the claim was made.")
    claim_location = models.CharField(max_length=255, help_text="The location where the claim was made.")
    claim_first_appearance = models.CharField(max_length=255, null=True, help_text="Link to where the claim first appeared.")
    claim_phrase = models.CharField(max_length=255, null=True, help_text="Claim phrase that we should track.")
    claim_author = models.CharField(max_length=255, help_text="The author of the claim")
    rating = models.BooleanField(default=False, help_text="Is the claim true or false")
    sheet_row = models.CharField(max_length=255, help_text="The sheet row in which this claim belongs to")
    processed = models.BooleanField(
        default=False,
        help_text="Determines if we've processed tweets related to this claim or not")

    def __str__(self):
        return self.claim_first_appearance or self.claim_phrase or ""

class MessageTemplate(models.Model):
    message_template =  models.CharField(max_length=255, help_text="Message template to use for sending reply")

    def __str__(self):
        return self.message_template
