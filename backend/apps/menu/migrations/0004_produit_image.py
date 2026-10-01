from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0003_ensure_composition_menu"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="produits/%Y/%m/"),
        ),
    ]
