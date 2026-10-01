import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("restaurant", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Categorie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("nom", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("ordre_affichage", models.SmallIntegerField(default=0)),
                ("image", models.CharField(blank=True, max_length=255)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="categories", to="restaurant.restaurant")),
            ],
            options={"db_table": "categorie", "ordering": ["ordre_affichage", "nom"]},
        ),
        migrations.CreateModel(
            name="Produit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("nom", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True)),
                ("prix", models.DecimalField(decimal_places=2, max_digits=10)),
                ("photo", models.CharField(blank=True, max_length=255)),
                ("disponible", models.BooleanField(default=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("date_modification", models.DateTimeField(auto_now=True)),
                ("categorie", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="produits", to="menu.categorie")),
            ],
            options={"db_table": "produit", "ordering": ["nom"]},
        ),
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("nom", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True)),
                ("prix", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date_debut", models.DateField(blank=True, null=True)),
                ("date_fin", models.DateField(blank=True, null=True)),
                ("disponible", models.BooleanField(default=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="menus", to="restaurant.restaurant")),
            ],
            options={"db_table": "menu"},
        ),
        migrations.CreateModel(
            name="CompositionMenu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantite", models.SmallIntegerField(default=1)),
                ("menu", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="menu.menu")),
                ("produit", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="menu.produit")),
            ],
            options={"db_table": "composition_menu"},
        ),
        migrations.AddField(
            model_name="menu",
            name="produits",
            field=models.ManyToManyField(related_name="menus", through="menu.CompositionMenu", to="menu.produit"),
        ),
        migrations.AddConstraint(
            model_name="compositionmenu",
            constraint=models.UniqueConstraint(fields=("menu", "produit"), name="produit_unique_par_menu"),
        ),
    ]
