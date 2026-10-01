from django.db import migrations


def create_composition_menu_if_missing(apps, schema_editor):
    """Restore the through table when the initial menu schema predates migrations."""
    CompositionMenu = apps.get_model("menu", "CompositionMenu")
    existing_tables = schema_editor.connection.introspection.table_names()

    if CompositionMenu._meta.db_table not in existing_tables:
        schema_editor.create_model(CompositionMenu)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("menu", "0002_seed_categories_initiales"),
    ]

    operations = [
        migrations.RunPython(create_composition_menu_if_missing, migrations.RunPython.noop),
    ]
