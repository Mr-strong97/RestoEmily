from django.contrib import admin

from .models import Alerte


@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ("type", "table", "statut", "date_creation", "traite_par")
    list_filter = ("type", "statut")
    list_select_related = ("table", "commande", "traite_par")
    readonly_fields = ("uuid", "date_creation", "date_traitement")
