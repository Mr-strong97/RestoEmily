from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("administrateurs", "0006_alter_administrateur_email")]

    operations = [
        migrations.AlterField(
            model_name="administrateur",
            name="statut",
            field=models.CharField(
                choices=[
                    ("actif", "Actif"),
                    ("inactif", "Inactif"),
                    ("bloque", "Bloqué"),
                ],
                default="inactif",
                max_length=20,
            ),
        ),
    ]
