import secrets

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.administrateurs.permissions import EstSuperAdmin

from .models import QRCode, Table
from .serializers import QRCodeResolveSerializer, TableCreateSerializer, TableSerializer


class TableListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        tables = Table.objects.filter(restaurant=request.user.restaurant)
        return Response(TableSerializer(tables, many=True).data)

    def post(self, request):
        serializer = TableCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table = serializer.save(restaurant=request.user.restaurant)
        return Response(TableSerializer(table).data, status=status.HTTP_201_CREATED)


class TableDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [permissions.IsAuthenticated()]

    def get(self, request, table_uuid):
        table = get_object_or_404(Table, uuid=table_uuid, restaurant=request.user.restaurant)
        return Response(TableSerializer(table).data)

    def patch(self, request, table_uuid):
        table = get_object_or_404(Table, uuid=table_uuid, restaurant=request.user.restaurant)
        nouveau_statut = request.data.get("statut")
        if nouveau_statut not in dict(Table.STATUT_CHOICES):
            return Response({"detail": "Statut invalide."}, status=status.HTTP_400_BAD_REQUEST)
        table.statut = nouveau_statut
        table.save(update_fields=["statut"])
        return Response(TableSerializer(table).data)

    def delete(self, request, table_uuid):
        get_object_or_404(Table, uuid=table_uuid, restaurant=request.user.restaurant).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegenererQRCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated, EstSuperAdmin]

    def post(self, request, table_uuid):
        table = get_object_or_404(Table, uuid=table_uuid, restaurant=request.user.restaurant)
        QRCode.objects.filter(table=table, statut="actif").update(statut="inactif")
        code_unique = secrets.token_hex(16)
        base_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        QRCode.objects.create(
            table=table, code_unique=code_unique,
            url_destination=f"{base_url}/table?code={code_unique}",
        )
        return Response(TableSerializer(table).data, status=status.HTTP_201_CREATED)


class QRCodeResolveView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code_unique):
        try:
            qrcode = QRCode.objects.select_related("table").get(code_unique=code_unique)
        except QRCode.DoesNotExist:
            return Response({"detail": "QR code invalide."}, status=status.HTTP_404_NOT_FOUND)
        if qrcode.statut != "actif":
            return Response({"detail": "Ce QR code n'est plus valide."}, status=status.HTTP_410_GONE)
        return Response(QRCodeResolveSerializer(qrcode).data)
