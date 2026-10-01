from django.db.models.deletion import ProtectedError
from rest_framework import generics, permissions, serializers
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from apps.administrateurs.permissions import EstSuperAdmin, PeutGererMenu

from .models import Categorie, Menu, Produit
from .serializers import (
    CategorieAdminSerializer, CategorieSerializer, MenuAdminSerializer,
    MenuFormuleSerializer, ProduitAdminSerializer, ProduitDetailSerializer,
)


class CarteView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Categorie.objects.prefetch_related("produits").all()
        menus = Menu.objects.filter(disponible=True).prefetch_related("produits")
        serializer_context = {"request": request}
        return Response({
            "categories": CategorieSerializer(categories, many=True, context=serializer_context).data,
            "formules": MenuFormuleSerializer(menus, many=True, context=serializer_context).data,
        })


class CategorieAdminListCreateView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieAdminSerializer
    permission_classes = [PeutGererMenu]

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)


class CategorieAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieAdminSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "categorie_uuid"

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [PeutGererMenu()]


class ProduitAdminListCreateView(generics.ListCreateAPIView):
    queryset = Produit.objects.select_related("categorie").all()
    serializer_class = ProduitAdminSerializer
    permission_classes = [PeutGererMenu]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        qs = super().get_queryset().filter(categorie__restaurant=self.request.user.restaurant)
        categorie_uuid = self.request.query_params.get("categorie")
        return qs.filter(categorie__uuid=categorie_uuid) if categorie_uuid else qs

    def perform_create(self, serializer):
        if serializer.validated_data["categorie"].restaurant_id != self.request.user.restaurant_id:
            raise serializers.ValidationError({"categorie_id": "Cette catégorie n'appartient pas à votre restaurant."})
        serializer.save()


class ProduitAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.select_related("categorie").all()
    serializer_class = ProduitAdminSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "produit_uuid"
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return super().get_queryset().filter(categorie__restaurant=self.request.user.restaurant)

    def perform_update(self, serializer):
        categorie = serializer.validated_data.get("categorie")
        if categorie and categorie.restaurant_id != self.request.user.restaurant_id:
            raise serializers.ValidationError({"categorie_id": "Cette catégorie n'appartient pas à votre restaurant."})
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "Ce produit est déjà lié à une commande et ne peut pas être supprimé. Désactive-le plutôt pour le retirer de la carte."}, status=400)

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [PeutGererMenu()]


class MenuAdminListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.prefetch_related("produits").all()
    serializer_class = MenuAdminSerializer
    permission_classes = [PeutGererMenu]

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        produits = serializer.validated_data.get("produits", [])
        if any(produit.categorie.restaurant_id != self.request.user.restaurant_id for produit in produits):
            raise serializers.ValidationError({"produit_ids": "Tous les produits doivent appartenir à votre restaurant."})
        serializer.save(restaurant=self.request.user.restaurant)


class MenuAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.prefetch_related("produits").all()
    serializer_class = MenuAdminSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "menu_uuid"

    def get_queryset(self):
        return super().get_queryset().filter(restaurant=self.request.user.restaurant)

    def perform_update(self, serializer):
        produits = serializer.validated_data.get("produits")
        if produits is not None and any(
            produit.categorie.restaurant_id != self.request.user.restaurant_id
            for produit in produits
        ):
            raise serializers.ValidationError({"produit_ids": "Tous les produits doivent appartenir à votre restaurant."})
        serializer.save()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), EstSuperAdmin()]
        return [PeutGererMenu()]

class ProduitDetailPublicView(generics.RetrieveAPIView):
    """GET /api/menu/produits/<uuid>/ — PUBLIC. Fiche détail d'un produit."""
    queryset = Produit.objects.filter(disponible=True).select_related("categorie")
    serializer_class = ProduitDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "uuid"
    lookup_url_kwarg = "produit_uuid"
