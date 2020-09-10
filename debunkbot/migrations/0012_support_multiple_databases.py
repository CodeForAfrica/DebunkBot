# Generated by Django 2.2 on 2020-09-10 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0011_responsemode"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClaimsDatabase",
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
                    "name",
                    models.CharField(
                        help_text="The name of the claims database",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(
                        default=False, help_text="Mark this claims database as deleted."
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="gsheetclaimsdatabase", name="claim_db_name",
        ),
        migrations.RemoveField(model_name="gsheetclaimsdatabase", name="deleted",),
        migrations.RemoveField(model_name="gsheetclaimsdatabase", name="id",),
        migrations.AlterField(
            model_name="messagetemplate",
            name="message_template_category",
            field=models.CharField(
                blank=True,
                help_text="Category that this message template belongs to.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gsheetclaimsdatabase",
            name="claimsdatabase_ptr",
            field=models.OneToOneField(
                auto_created=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="debunkbot.ClaimsDatabase",
            ),
            preserve_default=False,
        ),
    ]
