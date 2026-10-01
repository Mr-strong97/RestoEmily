from rest_framework import serializers
from apps.tables.models import QRCode
from .models import Alerte


class AlerteCreateSerializer(serializers.ModelSerializer):
    """Le client envoie son code_qr (jamais un table_id, falsifiable) ;
    on retrouve la table légitime en le revérifiant côté serveur."""
    code_qr = serializers.CharField(write_only=True)

    class Meta:
        model = Alerte
        fields = ["id", "code_qr", "type", "message"]
        read_only_fields = ["id"]

    def validate_code_qr(self, value):
        try:
            qrcode = QRCode.objects.select_related("table").get(code_unique=value, statut="actif")
        except QRCode.DoesNotExist:
            raise serializers.ValidationError("Contexte de table invalide ou expiré.")
        self._table = qrcode.table
        return value

    def create(self, validated_data):
        validated_data.pop("code_qr")
        return Alerte.objects.create(table=self._table, **validated_data)


class AlerteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    table_numero = serializers.IntegerField(source="table.numero", read_only=True)
    traite_par_nom = serializers.SerializerMethodField()

    class Meta:
        model = Alerte
        fields = ["id", "table_numero", "type", "message", "statut", "date_creation", "date_traitement", "traite_par_nom"]

    def get_traite_par_nom(self, alerte):
        return f"{alerte.traite_par.prenom} {alerte.traite_par.nom}" if alerte.traite_par else None