import uuid

import django.db.models.deletion
from django.db import migrations, models


def renseigner_commandes_existantes(apps, schema_editor):
    Commande = apps.get_model("commandes", "Commande")
    for commande in Commande.objects.filter(numero_commande__isnull=True).iterator():
        commande.numero_commande = f"LEGACY-{commande.pk}"
        commande.date_heure = commande.date_creation
        commande.save(update_fields=("numero_commande", "date_heure"))


class Migration(migrations.Migration):
    dependencies = [
        ("commandes", "0001_initial"),
        ("menu", "0001_initial"),
        ("tables", "0005_restaurant_fk_et_remap_valeurs"),
    ]

    operations = [
        migrations.AddField(model_name="commande", name="numero_commande", field=models.CharField(blank=True, max_length=30, null=True, unique=True)),
        migrations.AddField(model_name="commande", name="date_heure", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="commande", name="statut", field=models.CharField(choices=[("nouvelle", "Nouvelle"), ("confirmee", "Confirmée"), ("en_preparation", "En préparation"), ("prete", "Prête"), ("terminee", "Terminée"), ("annulee", "Annulée")], default="nouvelle", max_length=20)),
        migrations.AddField(model_name="commande", name="total", field=models.DecimalField(decimal_places=2, default=0, max_digits=10)),
        migrations.AlterField(model_name="commande", name="table", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="commandes", to="tables.table")),
        migrations.RunPython(renseigner_commandes_existantes, migrations.RunPython.noop),
        migrations.RemoveField(model_name="commande", name="date_creation"),
        migrations.AlterField(model_name="commande", name="numero_commande", field=models.CharField(max_length=30, unique=True)),
        migrations.AlterField(model_name="commande", name="date_heure", field=models.DateTimeField(auto_now_add=True)),
        migrations.AlterModelOptions(name="commande", options={"ordering": ["-date_heure"]}),
        migrations.CreateModel(
            name="LigneCommande",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("quantite", models.PositiveSmallIntegerField()),
                ("prix_unitaire", models.DecimalField(decimal_places=2, max_digits=10)),
                ("sous_total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("commande", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lignes", to="commandes.commande")),
                ("produit", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lignes_commande", to="menu.produit")),
            ],
            options={"db_table": "ligne_commande"},
        ),
    ]
