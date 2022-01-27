# Generated by Django 2.2.26 on 2022-01-27 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0025_auto_20220118_0638"),
    ]

    operations = [
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="claim_publication_column_name",
            field=models.CharField(
                blank=True,
                help_text="The column that contains claim publication date",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="platform_publication_column_name",
            field=models.CharField(
                blank=True,
                help_text="The column that contains platform publication date",
                max_length=255,
                null=True,
            ),
        ),
    ]
