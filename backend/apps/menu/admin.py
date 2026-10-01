from django.contrib import admin

from .models import Categorie, CompositionMenu, Menu, Produit


admin.site.register((Categorie, Produit, Menu, CompositionMenu))
