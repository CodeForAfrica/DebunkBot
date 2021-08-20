from django.db import migrations


def add_default_databasepriority(apps, schema_editor):
    DatabasePriority = apps.get_model("debunkbot", "DatabasePriority")
    db_alias = schema_editor.connection.alias
    DatabasePriority.objects.using(db_alias).create(
        active=True, low=33, normal=33, high=34
    )


class Migration(migrations.Migration):

    dependencies = [
        ("debunkbot", "0023_active_databasepriority"),
    ]
    operations = [
        migrations.RunPython(add_default_databasepriority),
    ]
