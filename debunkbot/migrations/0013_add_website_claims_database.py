# Generated by Django 2.2 on 2020-09-10 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0012_support_multiple_databases"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebsiteClaimDatabase",
            fields=[
                (
                    "claimsdatabase_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="debunkbot.ClaimsDatabase",
                    ),
                ),
                ("url", models.URLField(unique=True)),
            ],
            bases=("debunkbot.claimsdatabase",),
        ),
    ]
