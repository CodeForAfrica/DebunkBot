# Generated by Django 2.2 on 2020-06-15 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0007_googlesheetcredentials'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoreListGsheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='The key of the google sheet holding the ignore list.', max_length=255)),
                ('worksheet_name', models.CharField(help_text='The name of the workspace containing the ignore list', max_length=255)),
                ('column_name', models.CharField(help_text='The column name containing the ignore list.', max_length=255)),
            ],
        ),
    ]