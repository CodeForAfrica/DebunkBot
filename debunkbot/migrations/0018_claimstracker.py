# Generated by Django 2.2 on 2020-10-05 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0017_gsheetclaimsdatabase_claim_date_column_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClaimsTracker",
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
                ("total_claims", models.IntegerField(default=0)),
                ("current_offset", models.IntegerField(default=0)),
                (
                    "claim_db",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="debunkbot.ClaimsDatabase",
                    ),
                ),
            ],
        ),
    ]
