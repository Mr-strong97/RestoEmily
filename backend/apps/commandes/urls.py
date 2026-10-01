
from django.urls import path
from .views import CommandeChangerStatutView, CommandeCreateView, CommandeListeAdminView, CommandeSuiviView, DashboardView

urlpatterns = [
    path("", CommandeCreateView.as_view(), name="commande-create"),
    path("admin/", CommandeListeAdminView.as_view(), name="commande-liste-admin"),
    path("admin/<uuid:commande_uuid>/statut/", CommandeChangerStatutView.as_view(), name="commande-changer-statut"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("<uuid:commande_uuid>/", CommandeSuiviView.as_view(), name="commande-suivi"),
]