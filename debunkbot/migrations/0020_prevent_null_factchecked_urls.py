# Generated by Django 2.2 on 2020-12-06 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0019_allow_blank_claim_appearances"),
    ]

    operations = [
        migrations.AlterField(
            model_name="claim",
            name="fact_checked_url",
            field=models.TextField(
                default="", help_text="The URL to the debunked claim."
            ),
            preserve_default=False,
        ),
    ]
