# Generated by Django 2.2 on 2020-05-18 04:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0001_add_tweet_model"),
    ]
    operations = [
        migrations.CreateModel(
            name="Claim",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fact_checked_url",
                    models.TextField(help_text="The URL to the debunked claim."),
                ),
                (
                    "claim_reviewed",
                    models.TextField(help_text="The claim that has been debunked."),
                ),
                (
                    "claim_date",
                    models.CharField(
                        help_text="The date when the claim was made.", max_length=255
                    ),
                ),
                (
                    "claim_location",
                    models.CharField(
                        help_text="The location where the claim was made.",
                        max_length=255,
                    ),
                ),
                (
                    "claim_first_appearance",
                    models.TextField(
                        help_text="Link to where the claim first appeared.", null=True
                    ),
                ),
                (
                    "claim_appearances",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.TextField(),
                        help_text=(
                            "Links to where the claims appeared, comma separated."
                        ),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "claim_phrase",
                    models.CharField(
                        help_text="Claim phrase that we should track.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "claim_author",
                    models.CharField(
                        help_text="The author of the claim", max_length=255
                    ),
                ),
                (
                    "rating",
                    models.BooleanField(
                        default=False, help_text="Is the claim true or false?"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        help_text="The category to which this claim belongs to.",
                        max_length=255,
                        default="MISINFO",
                        blank=True,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="tweet",
            name="claim",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tweets",
                to="debunkbot.Claim",
            ),
        ),
        migrations.AddField(
            model_name="claim",
            name="processed",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Determines if we've processed tweets related to this claim "
                    "or not"
                ),
            ),
        ),
    ]
