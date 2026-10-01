from django.contrib import admin

from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "email")
    search_fields = ("nom", "adresse", "email")
