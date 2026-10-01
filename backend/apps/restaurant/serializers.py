from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["nom", "adresse", "telephone", "email", "description", "logo", "banniere", "horaires_ouverture"]