from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = Service
        fields = ["id", "nom", "description", "prix", "disponible"]


class ServiceAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = Service
        fields = ["id", "nom", "description", "prix", "disponible"]

    def create(self, validated_data):
        from apps.restaurant.models import Restaurant
        restaurant = validated_data.pop("restaurant", None) or Restaurant.instance()
        return Service.objects.create(restaurant=restaurant, **validated_data)
