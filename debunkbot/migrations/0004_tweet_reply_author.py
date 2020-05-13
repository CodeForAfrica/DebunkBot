# Generated by Django 2.2 on 2020-05-13 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debunkbot', '0003_auto_20200512_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='reply_author',
            field=models.CharField(default=1, help_text='The twitter handle of the person who sent the reply', max_length=255),
            preserve_default=False,
        ),
    ]
