import uuid

from django.db import migrations, models


def remplir_uuids(apps, schema_editor):
    """Attribue un UUID distinct à chaque administrateur déjà existant."""
    Administrateur = apps.get_model("administrateurs", "Administrateur")
    for administrateur in Administrateur.objects.filter(uuid__isnull=True).iterator():
        administrateur.uuid = uuid.uuid4()
        administrateur.save(update_fields=["uuid"])


class Migration(migrations.Migration):
    dependencies = [
        ("administrateurs", "0001_initial"),
    ]

    operations = [
        # nullable temporairement : la migration peut ainsi s'appliquer aux
        # comptes déjà présents, puis les valeurs sont remplies ci-dessous.
        migrations.AddField(
            model_name="administrateur",
            name="uuid",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(remplir_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="administrateur",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
