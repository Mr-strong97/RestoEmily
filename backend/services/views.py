from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.administrateurs.permissions import EstSuperAdmin, PeutGererMenu

from .models import Service
from .serializers import ServiceAdminSerializer, ServiceSerializer


class ServiceListPubliqueView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(ServiceSerializer(Service.objects.filter(disponible=True), many=True).data)


class ServiceAdminListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceAdminSerializer
    permission_classes = [PeutGererMenu]

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)


class ServiceAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceAdminSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "service_uuid"

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [PeutGererMenu()]
