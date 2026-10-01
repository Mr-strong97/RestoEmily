from django.contrib import admin
from .models import Administrateur

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ["email", "nom", "prenom", "role", "statut", "date_creation"]
    list_filter = ["role", "statut"]