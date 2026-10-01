from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantInfoView(APIView):
    """GET /api/restaurant/ — PUBLIC. Infos publiques (mono-restaurant)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        restaurant = Restaurant.instance()
        return Response(RestaurantSerializer(restaurant).data if restaurant else {})