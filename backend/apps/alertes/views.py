from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from .models import Alerte
from .serializers import AlerteCreateSerializer, AlerteSerializer


class AlerteCreateThrottle(AnonRateThrottle):
    scope = "alerte_creation"
    rate = "10/min"


class AlerteListCreateView(APIView):
    def get_permissions(self):
        return [permissions.AllowAny()] if self.request.method == "POST" else [permissions.IsAuthenticated()]

    def get_throttles(self):
        return [AlerteCreateThrottle()] if self.request.method == "POST" else []

    def post(self, request):
        serializer = AlerteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alerte = serializer.save()
        return Response(AlerteSerializer(alerte).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        alertes = Alerte.objects.filter(table__restaurant=request.user.restaurant).exclude(
            statut="traitee"
        ).select_related("table", "traite_par")
        return Response(AlerteSerializer(alertes, many=True).data)


class AlerteTraiterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, alerte_uuid):
        try:
            alerte = Alerte.objects.get(
                uuid=alerte_uuid,
                table__restaurant=request.user.restaurant,
            )
        except Alerte.DoesNotExist:
            return Response({"detail": "Alerte introuvable."}, status=status.HTTP_404_NOT_FOUND)
        nouveau_statut = request.data.get("statut")
        if nouveau_statut not in ("prise_en_charge", "traitee"):
            return Response({"detail": "Statut invalide."}, status=status.HTTP_400_BAD_REQUEST)
        alerte.statut = nouveau_statut
        alerte.traite_par = request.user
        if nouveau_statut == "traitee":
            alerte.date_traitement = timezone.now()
        alerte.save()
        return Response(AlerteSerializer(alerte).data)
