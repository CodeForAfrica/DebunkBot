# Generated by Django 2.2 on 2020-05-18 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0001_add_tweet_model'),
    ]
    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fact_checked_url', models.CharField(help_text='The URL to the debunked claim.', max_length=255)),
                ('claim_reviewed', models.CharField(help_text='The claim that has been debunked.', max_length=255)),
                ('claim_date', models.CharField(help_text='The date when the claim was made.', max_length=255)),
                ('claim_location', models.CharField(help_text='The location where the claim was made.', max_length=255)),
                ('claim_appearances', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), help_text='Links to where the claims appeared.', null=True, size=None)),
                ('claim_phrase', models.CharField(help_text='Claim phrase that we should track.', max_length=255, null=True)),
                ('claim_author', models.CharField(help_text='The author of the claim', max_length=255)),
                ('rating', models.BooleanField(default=False, help_text='Is the claim true or false')),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='claim',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tweets', to='debunkbot.Claim'),
        ),
        migrations.AddField(
            model_name='claim',
            name='processed',
            field=models.BooleanField(
                default=False,
                help_text="Determines if we've processed tweets related to this claim or not"),
        ),
    ]
