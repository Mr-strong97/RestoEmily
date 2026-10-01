from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import EstSuperAdmin
from .serializers import (
    AdministrateurCreationSerializer,
    AdministrateurGestionSerializer,
    AdministrateurSerializer,
    ConnexionSerializer,
    InscriptionSerializer,
)
from .models import Administrateur


class InscriptionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        administrateur = serializer.save()
        return Response(AdministrateurSerializer(administrateur).data, status=status.HTTP_201_CREATED)


class ConnexionView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ConnexionSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class DeconnexionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Le jeton refresh est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
        except Exception:
            return Response({"detail": "Jeton refresh invalide."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class MoiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(AdministrateurSerializer(request.user).data)


class AdministrateurListCreateView(generics.ListCreateAPIView):
    queryset = Administrateur.objects.all().order_by("-date_creation")
    permission_classes = [permissions.IsAuthenticated, EstSuperAdmin]

    def get_serializer_class(self):
        return AdministrateurCreationSerializer if self.request.method == "POST" else AdministrateurGestionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        administrateur = serializer.save(restaurant=request.user.restaurant)
        return Response(AdministrateurGestionSerializer(administrateur).data, status=status.HTTP_201_CREATED)


class AdministrateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurGestionSerializer
    permission_classes = [permissions.IsAuthenticated, EstSuperAdmin]
    lookup_field = "id"
    lookup_url_kwarg = "administrateur_uuid"

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def patch(self, request, *args, **kwargs):
        cible = self.get_object()
        if cible.pk == request.user.pk and ("statut" in request.data or "role" in request.data):
            return Response(
                {"detail": "Tu ne peux pas modifier ton propre rôle ou statut. Demande à un autre Super Admin."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cible = self.get_object()
        if cible.pk == request.user.pk:
            return Response(
                {"detail": "Tu ne peux pas supprimer ton propre compte."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if cible.role == "super_admin":
            autres = Administrateur.objects.filter(
                restaurant=request.user.restaurant, role="super_admin", statut="actif"
            ).exclude(pk=cible.pk)
            if not autres.exists():
                return Response(
                    {"detail": "Impossible de supprimer le dernier Super Administrateur actif."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().destroy(request, *args, **kwargs)
