# Generated by Django 2.2 on 2020-09-15 05:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("debunkbot", "0015_rename_model_key_to_sheet_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="claim",
            name="claim_date",
            field=models.DateField(
                blank=True, help_text="The date when the claim was made.", null=True
            ),
        ),
    ]
