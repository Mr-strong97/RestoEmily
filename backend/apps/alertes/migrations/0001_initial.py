import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alerte",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("type", models.CharField(choices=[("appel_serveur", "Appel serveur"), ("demande_addition", "Demande d'addition"), ("autre", "Autre")], default="appel_serveur", max_length=30)),
                ("message", models.CharField(blank=True, max_length=280)),
                ("statut", models.CharField(choices=[("nouvelle", "Nouvelle"), ("prise_en_charge", "Prise en charge"), ("traitee", "Traitée")], default="nouvelle", max_length=20)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_traitement", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "alerte", "ordering": ["-date_creation"]},
        ),
    ]
