import uuid as uuid_lib
from django.db import models


class Categorie(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ordre_affichage = models.SmallIntegerField(default=0)
    image = models.CharField(max_length=255, blank=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", on_delete=models.PROTECT, related_name="categories")

    class Meta:
        db_table = "categorie"
        ordering = ["ordre_affichage", "nom"]

    def __str__(self):
        return self.nom


class Produit(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="produits/%Y/%m/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="produits")

    class Meta:
        db_table = "produit"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def delete(self, *args, **kwargs):
        """Delete the uploaded file when a product is removed from the API."""
        storage, name = self.image.storage, self.image.name
        super().delete(*args, **kwargs)
        if name:
            storage.delete(name)


class Menu(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", on_delete=models.PROTECT, related_name="menus")
    produits = models.ManyToManyField(Produit, through="CompositionMenu", related_name="menus")

    class Meta:
        db_table = "menu"

    def __str__(self):
        return self.nom


class CompositionMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.SmallIntegerField(default=1)

    class Meta:
        db_table = "composition_menu"
        constraints = [models.UniqueConstraint(fields=["menu", "produit"], name="produit_unique_par_menu")]
