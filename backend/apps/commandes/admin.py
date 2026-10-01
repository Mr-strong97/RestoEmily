from django.contrib import admin

from .models import Commande, LigneCommande


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ("numero_commande", "table", "statut", "total", "date_heure")
    list_select_related = ("table",)
    readonly_fields = ("uuid", "date_heure")


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = ("commande", "produit", "quantite", "prix_unitaire", "sous_total")
    list_select_related = ("commande", "produit")
