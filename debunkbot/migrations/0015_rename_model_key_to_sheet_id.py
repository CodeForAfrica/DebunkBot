# Generated by Django 2.2 on 2020-09-15 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0014_allow_some_claim_fields_to_be_blank"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gsheetclaimsdatabase", old_name="key", new_name="spreadsheetId",
        ),
        migrations.RenameField(
            model_name="ignorelistgsheet", old_name="key", new_name="spreadsheetId",
        ),
        migrations.RenameField(
            model_name="messagetemplatesource",
            old_name="key",
            new_name="spreadsheetId",
        ),
        migrations.RenameField(
            model_name="respondlistgsheet", old_name="key", new_name="spreadsheetId",
        ),
    ]
