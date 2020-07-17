# Generated by Django 2.2 on 2020-06-15 01:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0006_gsheetclaimsdatabase'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleSheetCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credentials', django.contrib.postgres.fields.jsonb.JSONField(help_text="The service account key needed by the application to access Google Sheet data.")),
            ],
        ),
    ]
