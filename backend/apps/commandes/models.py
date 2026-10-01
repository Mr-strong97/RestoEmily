import uuid as uuid_lib
from django.db import models
from apps.tables.models import Table


class Commande(models.Model):
    STATUT_CHOICES = [
        ("nouvelle", "Nouvelle"), ("confirmee", "Confirmée"), ("en_preparation", "En préparation"),
        ("prete", "Prête"), ("terminee", "Terminée"), ("annulee", "Annulée"),
    ]

    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name="commandes")
    numero_commande = models.CharField(max_length=30, unique=True)
    date_heure = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="nouvelle")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "commande"
        ordering = ["-date_heure"]

    def __str__(self):
        return f"Commande {self.numero_commande}"

    def recalculer_total(self):
        self.total = self.lignes.aggregate(s=models.Sum("sous_total"))["s"] or 0
        self.save(update_fields=["total"])


class LigneCommande(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey("menu.Produit", on_delete=models.PROTECT, related_name="lignes_commande")
    quantite = models.PositiveSmallIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "ligne_commande"

    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"