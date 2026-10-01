from django.db.models import Count, F, Sum
from django.db.models.functions import TruncHour
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Commande, LigneCommande
from .serializers import CommandeCreateSerializer, CommandeSerializer


class CommandeCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CommandeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commande = serializer.save()
        return Response(CommandeSerializer(commande).data, status=status.HTTP_201_CREATED)


class CommandeSuiviView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, commande_uuid):
        commande = get_object_or_404(Commande, uuid=commande_uuid)
        return Response(CommandeSerializer(commande).data)


class DashboardView(APIView):
    """Indicateurs du jour visibles par les administrateurs authentifiés."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from apps.alertes.models import Alerte
        from apps.tables.models import Table

        today = timezone.localdate()
        restaurant = request.user.restaurant
        commandes_du_jour = Commande.objects.filter(
            date_heure__date=today,
            table__restaurant=restaurant,
        ).exclude(statut="annulee")

        nombre_commandes = commandes_du_jour.count()
        chiffre_affaires = commandes_du_jour.aggregate(total=Sum("total"))["total"] or 0
        tables = Table.objects.filter(restaurant=restaurant)
        tables_occupees = tables.filter(statut="occupee")

        flux_horaire = list(
            commandes_du_jour.annotate(heure=TruncHour("date_heure"))
            .values("heure")
            .annotate(nombre=Count("id"))
            .order_by("heure")
        )
        repartition_ventes = list(
            LigneCommande.objects.filter(commande__in=commandes_du_jour)
            .values(categorie=F("produit__categorie__nom"))
            .annotate(montant=Sum("sous_total"))
            .order_by("-montant")
        )
        alertes = Alerte.objects.exclude(statut="traitee").filter(
            table__restaurant=restaurant
        ).select_related("table")[:10]

        return Response({
            "chiffre_affaires": float(chiffre_affaires),
            "nombre_commandes": nombre_commandes,
            "panier_moyen": float(chiffre_affaires / nombre_commandes) if nombre_commandes else 0,
            "tables_occupees": tables_occupees.count(),
            "tables_total": tables.count(),
            "couverts": tables_occupees.aggregate(total=Sum("capacite"))["total"] or 0,
            "flux_horaire": [
                {"heure": item["heure"].strftime("%H:%M"), "nombre": item["nombre"]}
                for item in flux_horaire
            ],
            "repartition_ventes": [
                {"categorie": item["categorie"] or "Sans catégorie", "montant": float(item["montant"])}
                for item in repartition_ventes
            ],
            "alertes_actives": [
                {
                    "id": str(alerte.uuid),
                    "table_numero": alerte.table.numero,
                    "type": alerte.type,
                    "message": alerte.message,
                    "date_creation": alerte.date_creation,
                }
                for alerte in alertes
            ],
            "dernieres_commandes": [
                {
                    "id": str(commande.uuid),
                    "numero_commande": commande.numero_commande,
                    "total": str(commande.total),
                    "statut": commande.statut,
                    "table_numero": commande.table.numero if commande.table else None,
                }
                for commande in commandes_du_jour.select_related("table")[:10]
            ],
        })

class CommandeListeAdminView(APIView):
    """GET /api/commandes/admin/?statut=xxx — par défaut : actives (hors terminee/annulee)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        statut = request.query_params.get("statut")
        commandes = Commande.objects.filter(table__restaurant=request.user.restaurant)
        if statut:
            commandes = commandes.filter(statut=statut).select_related("table")
        else:
            commandes = commandes.exclude(statut__in=["terminee", "annulee"]).select_related("table")
        return Response(CommandeSerializer(commandes, many=True).data)


class CommandeChangerStatutView(APIView):
    """PATCH /api/commandes/admin/<uuid>/statut/ — ouvert à tout le personnel
    authentifié (tâche opérationnelle courante)."""
    permission_classes = [permissions.IsAuthenticated]
    STATUTS_TERMINAUX = ("terminee", "annulee")

    def patch(self, request, commande_uuid):
        commande = get_object_or_404(
            Commande,
            uuid=commande_uuid,
            table__restaurant=request.user.restaurant,
        )
        nouveau_statut = request.data.get("statut")

        if nouveau_statut not in dict(Commande.STATUT_CHOICES):
            return Response({"detail": "Statut invalide."}, status=status.HTTP_400_BAD_REQUEST)
        if commande.statut in self.STATUTS_TERMINAUX:
            return Response(
                {"detail": f"Commande déjà '{commande.statut}' — statut définitif, non modifiable."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        commande.statut = nouveau_statut
        commande.save(update_fields=["statut"])
        return Response(CommandeSerializer(commande).data)
