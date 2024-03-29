# Generated by Django 2.2 on 2020-07-15 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0008_ignorelistgsheet"),
    ]

    operations = [
        migrations.CreateModel(
            name="MessageTemplateSource",
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
                    "key",
                    models.CharField(
                        help_text=(
                            "The spreadsheet id from which we will be pulling message "
                            "templates from."
                        ),
                        max_length=255,
                    ),
                ),
                (
                    "worksheet",
                    models.CharField(
                        help_text=(
                            "The worksheet name from which the message templates will "
                            "be fetched."
                        ),
                        max_length=255,
                    ),
                ),
                (
                    "column",
                    models.CharField(
                        help_text="The column holding the message templates.",
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="message_template_source",
            field=models.ForeignKey(
                help_text="The message template source for this database.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="claims_databases",
                to="debunkbot.MessageTemplateSource",
            ),
        ),
        migrations.AddField(
            model_name="messagetemplate",
            name="message_template_source",
            field=models.ForeignKey(
                help_text="The source of the message templates.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="message_templates",
                to="debunkbot.MessageTemplateSource",
            ),
        ),
    ]
