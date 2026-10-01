import uuid as uuid_lib
from django.db import models
from apps.administrateurs.models import Administrateur
from apps.commandes.models import Commande
from apps.tables.models import Table


class Alerte(models.Model):
    TYPE_CHOICES = [
        ("appel_serveur", "Appel serveur"), ("demande_addition", "Demande d'addition"), ("autre", "Autre"),
    ]
    STATUT_CHOICES = [("nouvelle", "Nouvelle"), ("prise_en_charge", "Prise en charge"), ("traitee", "Traitée")]

    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="alertes")
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True, related_name="alertes")
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="appel_serveur")
    message = models.CharField(max_length=280, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="nouvelle")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    traite_par = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True, blank=True, related_name="alertes_traitees")

    class Meta:
        db_table = "alerte"
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Alerte {self.type} - Table {self.table.numero} ({self.statut})"