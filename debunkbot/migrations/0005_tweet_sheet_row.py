# Generated by Django 2.2 on 2020-05-13 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0004_tweet_reply_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='sheet_row',
            field=models.CharField(default=2, help_text='The sheet row in which this tweet belongs to', max_length=255),
            preserve_default=False,
        ),
    ]