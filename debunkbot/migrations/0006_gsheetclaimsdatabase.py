# Generated by Django 2.2 on 2020-06-08 11:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0005_message_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSheetClaimsDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text="The spreadsheet id for the database we're pulling from", max_length=255)),
                ('worksheets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), help_text='List of workspaces to fetch data from', size=None)),
                ('claim_url_column_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), help_text='List of columns to fetch claim urls from in this specific spreadsheet', size=None)),
                ('claim_phrase_column_name', models.CharField(help_text='The column to fetch claim phrases from in this specific spreadsheet', max_length=255)),
                ('claim_first_appearance_column_name', models.CharField(help_text='The column to fetch claim first appearance from in this specific spreadsheet', max_length=255)),
                ('claim_rating_column_name', models.CharField(help_text='The column to fetch claim rating from in this specific spreadsheet', max_length=255)),
                ('claim_description_column_name', models.CharField(help_text='The column to fetch claim checked from in this specific spreadsheet', max_length=255)),
                ('claim_debunk_url_column_name', models.CharField(help_text='The column to fetch claim debunked from in this specific spreadsheet', max_length=255)),
                ('claim_location_column_name', models.CharField(help_text='The column to fetch claim location from in this specific spreadsheet', max_length=255)),
                ('claim_author_column_name', models.CharField(help_text='The column to fetch claim author from in this specific spreadsheet', max_length=255)),
                ('claim_db_link', models.CharField(help_text='The link to the sheet storing the recorded claims.', max_length=255)),
                ('claim_db_name', models.CharField(help_text='The name of the sheet storing the recorded claims.', max_length=255)),
            ],
        ),
    ]
