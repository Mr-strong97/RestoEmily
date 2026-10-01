from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AdministrateurDetailView,
    AdministrateurListCreateView,
    ConnexionView,
    DeconnexionView,
    InscriptionView,
    MoiView,
)

urlpatterns = [
    path("inscription/", InscriptionView.as_view(), name="administrateur-inscription"),
    path("connexion/", ConnexionView.as_view(), name="administrateur-connexion"),
    path("connexion/refresh/", TokenRefreshView.as_view(), name="administrateur-refresh"),
    path("deconnexion/", DeconnexionView.as_view(), name="administrateur-deconnexion"),
    path("moi/", MoiView.as_view(), name="administrateur-moi"),
    path("gestion/", AdministrateurListCreateView.as_view(), name="administrateur-gestion-list"),
    path("gestion/<uuid:administrateur_uuid>/", AdministrateurDetailView.as_view(), name="administrateur-gestion-detail"),
]
