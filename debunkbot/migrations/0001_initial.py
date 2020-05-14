# Generated by Django 2.2 on 2020-05-11 05:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', django.contrib.postgres.fields.jsonb.JSONField()),
                ('responded', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tweets',
            },
        ),
    ]
