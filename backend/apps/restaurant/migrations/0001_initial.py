from django.db import migrations, models


def creer_restaurant_principal(apps, schema_editor):
    Restaurant = apps.get_model("restaurant", "Restaurant")
    Restaurant.objects.get_or_create(
        nom="Restaurant principal",
        defaults={"adresse": "À renseigner"},
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=150)),
                ("adresse", models.CharField(max_length=255)),
                ("telephone", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=150)),
                ("description", models.TextField(blank=True)),
                ("logo", models.CharField(blank=True, max_length=255)),
                ("banniere", models.CharField(blank=True, max_length=255)),
                ("horaires_ouverture", models.CharField(blank=True, max_length=255)),
            ],
            options={"db_table": "restaurant"},
        ),
        migrations.RunPython(creer_restaurant_principal, migrations.RunPython.noop),
    ]
