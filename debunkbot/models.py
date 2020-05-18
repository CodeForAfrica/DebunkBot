from django.contrib.postgres.fields import JSONField
from django.db import models


class Tweet(models.Model):
    tweet = JSONField()
    responded = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    reply_id = models.CharField(max_length=255, help_text="The Id of the reply we send to this tweet")
    reply_author = models.CharField(max_length=255, help_text="The twitter handle of the person who sent the reply")
    claim = models.ForeignKey('Claim', related_name='tweets', on_delete=models.SET_NULL, null=True)
    impact = JSONField(default=dict)

    def __str__(self):
        return self.tweet.get('text')
    class Meta:
        db_table = 'tweets'


class Claim(models.Model):
    url = models.CharField(max_length=255, help_text="The URL to the debunked claim.")
    claim_reviewed = models.CharField(max_length=255, help_text="The claim that has been debunked.")
    claim_date = models.CharField(max_length=255, help_text="The date when the claim was made.")
    claim_location = models.CharField(max_length=255, help_text="The location where the claim was made.")
    claim_first_appearance = models.CharField(max_length=255, help_text="Link to where the claim first appeared.")
    claim_author = models.CharField(max_length=255, help_text="The author of the claim")
    rating = models.BooleanField(default=False, help_text="Is the claim true or false")
    sheet_row = models.CharField(max_length=255, help_text="The sheet row in which this claim belongs to")

    def __str__(self):
        return self.claim_first_appearance
    