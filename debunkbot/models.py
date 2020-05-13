from django.contrib.postgres.fields import JSONField
from django.db import models


class Tweet(models.Model):
    tweet = JSONField()
    responded = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    reply_id = models.CharField(max_length=255, help_text="The Id of the reply we send to this tweet")
    reply_author = models.CharField(max_length=255, help_text="The twitter handle of the person who sent the reply")
    impact = JSONField(default=dict)
    sheet_row = models.CharField(max_length=255, help_text="The sheet row in which this tweet belongs to")

    def __str__(self):
        return self.tweet.get('text')
    class Meta:
        db_table = 'tweets'
