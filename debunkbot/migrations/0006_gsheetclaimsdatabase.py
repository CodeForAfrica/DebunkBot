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
                ('worksheets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), help_text='List of workspaces to fetch data from, comma separated', size=None)),
                ('claim_url_column_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), help_text='List of columns to fetch claim urls from in this specific spreadsheet, comma separated', size=None)),
                ('claim_phrase_column_name', models.CharField(help_text='The column to fetch claim phrases from in this specific spreadsheet', max_length=255, blank=True, null=True)),
                ('claim_first_appearance_column_name', models.CharField(help_text='The column to fetch claim first appearance from in this specific spreadsheet', max_length=255, blank=True, null=True)),
                ('claim_rating_column_name', models.CharField(help_text='The column to fetch claim rating from in this specific spreadsheet', max_length=255)),
                ('claim_description_column_name', models.CharField(help_text='The column to fetch claim checked from in this specific spreadsheet', max_length=255)),
                ('claim_debunk_url_column_name', models.CharField(help_text='The column to fetch claim debunked from in this specific spreadsheet', max_length=255, blank=True, null=True)),
                ('claim_location_column_name', models.CharField(help_text='The column to fetch claim location from in this specific spreadsheet', max_length=255, blank=True, null=True)),
                ('claim_author_column_name', models.CharField(help_text='The column to fetch claim author from in this specific spreadsheet', max_length=255, blank=True, null=True)),
                ('claim_db_name', models.CharField(help_text='The name of the sheet storing the recorded claims.', max_length=255, unique=True)),
                ('claim_category_name', models.CharField(help_text='The colum that contains claim category.', max_length=255, null=True, blank=True)),
                ('deleted', models.BooleanField(default=False, help_text='Mark this claims database as deleted.')),
            ],
        ),
        migrations.AddField(
            model_name='claim',
            name='claim_db',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='debunkbot.GSheetClaimsDatabase'),
        ),
        migrations.AlterModelOptions(
            name='gsheetclaimsdatabase',
            options={'verbose_name': 'GoogleSheetClaimsDatabase'},
        ),
    ]
