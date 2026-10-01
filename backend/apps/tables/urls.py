from django.urls import path
from .views import QRCodeResolveView, RegenererQRCodeView, TableDetailView, TableListCreateView

urlpatterns = [
    path("", TableListCreateView.as_view(), name="table-list-create"),
    path("<uuid:table_uuid>/", TableDetailView.as_view(), name="table-detail"),
    path("<uuid:table_uuid>/qrcode/regenerer/", RegenererQRCodeView.as_view(), name="table-qrcode-regenerer"),
    path("qrcodes/<str:code_unique>/", QRCodeResolveView.as_view(), name="qrcode-resolve"),
]