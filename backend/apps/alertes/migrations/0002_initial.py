import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("alertes", "0001_initial"),
        ("administrateurs", "0003_administrateur_id_uuid"),
        ("commandes", "0001_initial"),
        ("tables", "0004_uuid_unique_and_constraint"),
    ]

    operations = [
        migrations.AddField(
            model_name="alerte",
            name="commande",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="alertes", to="commandes.commande"),
        ),
        migrations.AddField(
            model_name="alerte",
            name="table",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alertes", to="tables.table"),
        ),
        migrations.AddField(
            model_name="alerte",
            name="traite_par",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="alertes_traitees", to="administrateurs.administrateur"),
        ),
    ]
