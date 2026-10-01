import uuid

from django.db import migrations, models


def remplir_uuids(apps, schema_editor):
    for nom_modele in ("Table", "QRCode"):
        modele = apps.get_model("tables", nom_modele)
        for objet in modele.objects.filter(uuid__isnull=True).iterator():
            objet.uuid = uuid.uuid4()
            objet.save(update_fields=["uuid"])


class Migration(migrations.Migration):
    dependencies = [("tables", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="table",
            name="uuid",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name="qrcode",
            name="uuid",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(remplir_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="table",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="qrcode",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
