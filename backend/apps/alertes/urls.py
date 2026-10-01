from django.urls import path
from .views import AlerteListCreateView, AlerteTraiterView

urlpatterns = [
    path("", AlerteListCreateView.as_view(), name="alerte-list-create"),
    path("<uuid:alerte_uuid>/traiter/", AlerteTraiterView.as_view(), name="alerte-traiter"),
]
