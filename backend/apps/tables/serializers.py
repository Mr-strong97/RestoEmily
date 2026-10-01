import secrets

from django.conf import settings
from rest_framework import serializers

from apps.restaurant.models import Restaurant
from .models import QRCode, Table


class QRCodeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = QRCode
        fields = ["id", "code_unique", "url_destination", "statut", "date_generation"]


class TableSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    qrcode = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ["id", "numero", "capacite", "statut", "qrcode"]

    def get_qrcode(self, table):
        qr = table.qrcodes.filter(statut="actif").first()
        return QRCodeSerializer(qr).data if qr else None


class TableInfoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = Table
        fields = ["id", "numero", "capacite", "statut"]


class QRCodeResolveSerializer(serializers.ModelSerializer):
    table = TableInfoSerializer(read_only=True)

    class Meta:
        model = QRCode
        fields = ["code_unique", "statut", "table"]


class TableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["capacite", "statut"]
        extra_kwargs = {"statut": {"required": False}}

    def create(self, validated_data):
        restaurant = validated_data.pop("restaurant", None) or Restaurant.instance()
        if restaurant is None:
            raise serializers.ValidationError("Créez d'abord un restaurant.")
        numero = Table.prochain_numero_disponible(restaurant)
        if numero is None:
            raise serializers.ValidationError(
                "Les 100 tables existent déjà — impossible d'en créer une de plus."
            )
        table = Table.objects.create(numero=numero, restaurant=restaurant, **validated_data)
        code_unique = secrets.token_hex(16)
        base_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        QRCode.objects.create(
            table=table, code_unique=code_unique,
            url_destination=f"{base_url}/table?code={code_unique}",
        )
        return table
