from django.urls import path
from .views import (
    CarteView, CategorieAdminDetailView, CategorieAdminListCreateView,
    MenuAdminDetailView, MenuAdminListCreateView, ProduitAdminDetailView, ProduitAdminListCreateView,
    ProduitDetailPublicView,
)

urlpatterns = [
    path("carte/", CarteView.as_view(), name="menu-carte"),
    path("admin/categories/", CategorieAdminListCreateView.as_view(), name="categorie-admin-list"),
    path("admin/categories/<uuid:categorie_uuid>/", CategorieAdminDetailView.as_view(), name="categorie-admin-detail"),
    path("admin/produits/", ProduitAdminListCreateView.as_view(), name="produit-admin-list"),
    path("admin/produits/<uuid:produit_uuid>/", ProduitAdminDetailView.as_view(), name="produit-admin-detail"),
    path("admin/menus/", MenuAdminListCreateView.as_view(), name="menu-admin-list"),
    path("admin/menus/<uuid:menu_uuid>/", MenuAdminDetailView.as_view(), name="menu-admin-detail"),
    path("produits/<uuid:produit_uuid>/", ProduitDetailPublicView.as_view(), name="produit-detail-public"),
]
