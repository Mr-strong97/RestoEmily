from rest_framework import serializers
from django.db import transaction
from apps.menu.models import Produit
from .models import Commande, LigneCommande


class LigneCommandeSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source="produit.nom", read_only=True)

    class Meta:
        model = LigneCommande
        fields = ["produit_nom", "quantite", "prix_unitaire", "sous_total"]


class CommandeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    lignes = LigneCommandeSerializer(many=True, read_only=True)
    table_numero = serializers.IntegerField(source="table.numero", read_only=True, default=None)

    class Meta:
        model = Commande
        fields = ["id", "numero_commande", "statut", "total", "date_heure", "table_numero", "lignes"]


class ArticlePanierSerializer(serializers.Serializer):
    produit_id = serializers.UUIDField()
    quantite = serializers.IntegerField(min_value=1)


class CommandeCreateSerializer(serializers.Serializer):
    code_qr = serializers.CharField()
    articles = ArticlePanierSerializer(many=True)

    def validate_code_qr(self, value):
        from apps.tables.models import QRCode
        try:
            qrcode = QRCode.objects.select_related("table").get(code_unique=value, statut="actif")
        except QRCode.DoesNotExist:
            raise serializers.ValidationError("Contexte de table invalide ou expiré.")
        self._table = qrcode.table
        return value

    def validate_articles(self, value):
        if not value:
            raise serializers.ValidationError("Le panier est vide.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        import secrets
        table = self._table
        produit_ids = [a["produit_id"] for a in validated_data["articles"]]
        produits = {
            produit.uuid: produit
            for produit in Produit.objects.filter(
                uuid__in=produit_ids,
                disponible=True,
                categorie__restaurant=table.restaurant,
            )
        }
        manquants = set(produit_ids) - set(produits.keys())
        if manquants:
            raise serializers.ValidationError({"articles": f"{len(manquants)} produit(s) indisponible(s) ou introuvable(s)."})

        commande = Commande.objects.create(table=table, numero_commande=f"T{table.numero}-{secrets.token_hex(3).upper()}")
        for article in validated_data["articles"]:
            produit = produits[article["produit_id"]]
            LigneCommande.objects.create(commande=commande, produit=produit, quantite=article["quantite"], prix_unitaire=produit.prix)
        commande.recalculer_total()
        return commande
