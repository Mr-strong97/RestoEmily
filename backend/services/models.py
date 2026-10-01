import uuid as uuid_lib
from django.db import models


def _restaurant_par_defaut():
    from django.db.utils import OperationalError, ProgrammingError
    try:
        from apps.restaurant.models import Restaurant
        r = Restaurant.objects.first()
        return r.pk if r else None
    except (OperationalError, ProgrammingError):
        return None


class Service(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)
    restaurant = models.ForeignKey("restaurant.Restaurant", on_delete=models.PROTECT, related_name="services", default=_restaurant_par_defaut)

    class Meta:
        db_table = "service"
        ordering = ["nom"]

    def __str__(self):
        return self.nom