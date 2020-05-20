# Generated by Django 2.2 on 2020-05-20 11:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0003_add_reply_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Impact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes_count', models.IntegerField(help_text='Number of people who have liked our reply.')),
                ('replies_count', models.IntegerField(help_text='Number of replies we have recieved on our reply.')),
                ('retweet_count', models.IntegerField(help_text='Number of retweets our reply has been retweeted.')),
                ('replies', models.TextField(help_text='All replies we have received on our reply.')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('tweet_deleted', models.BooleanField(default=False, help_text='Has the tweet we replied to been deleted?')),
                ('reply', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='debunkbot.Reply')),
            ],
        ),
    ]
