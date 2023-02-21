# Generated by Django 2.2.26 on 2022-01-18 06:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0024_createdefault_databasepriority"),
    ]

    operations = [
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="claims_ratings",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                default=["False"],
                help_text="List of ratings that a claim can have in this GSheet",
                size=None,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="claims_start_row",
            field=models.IntegerField(
                default=1, help_text="Row number where valid claims start from"
            ),
        ),
    ]
