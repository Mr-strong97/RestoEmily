from django.urls import path
from .views import ServiceAdminDetailView, ServiceAdminListCreateView, ServiceListPubliqueView

urlpatterns = [
    path("", ServiceListPubliqueView.as_view(), name="service-list-public"),
    path("admin/", ServiceAdminListCreateView.as_view(), name="service-admin-list"),
    path("admin/<uuid:service_uuid>/", ServiceAdminDetailView.as_view(), name="service-admin-detail"),
]