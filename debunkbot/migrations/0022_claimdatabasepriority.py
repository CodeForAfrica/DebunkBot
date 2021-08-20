# Generated by Django 2.2.24 on 2021-08-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0021_databasepriority"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="databasepriority",
            options={"verbose_name_plural": "Database Priorities"},
        ),
        migrations.AddField(
            model_name="claimsdatabase",
            name="priority",
            field=models.CharField(
                choices=[("low", "Low"), ("normal", "Normal"), ("high", "High")],
                default="normal",
                max_length=6,
            ),
        ),
    ]