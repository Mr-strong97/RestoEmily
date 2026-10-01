import uuid as uuid_lib
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def _restaurant_par_defaut():
    from django.db.utils import OperationalError, ProgrammingError
    try:
        from apps.restaurant.models import Restaurant
        r = Restaurant.objects.first()
        return r.pk if r else None
    except (OperationalError, ProgrammingError):
        return None


class Table(models.Model):
    STATUT_CHOICES = [("libre", "Libre"), ("occupee", "Occupée")]

    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    numero = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    capacite = models.PositiveSmallIntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="libre")
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.PROTECT, related_name="tables", default=_restaurant_par_defaut
    )

    class Meta:
        db_table = "table_restaurant"
        ordering = ["numero"]
        constraints = [models.UniqueConstraint(fields=["numero", "restaurant"], name="numero_unique_par_restaurant")]

    def __str__(self):
        return f"Table {self.numero}"

    @staticmethod
    def prochain_numero_disponible(restaurant):
        numeros_pris = set(Table.objects.filter(restaurant=restaurant).values_list("numero", flat=True))
        for n in range(1, 101):
            if n not in numeros_pris:
                return n
        return None


class QRCode(models.Model):
    STATUT_CHOICES = [("actif", "Actif"), ("inactif", "Inactif")]

    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="qrcodes")
    code_unique = models.CharField(max_length=64, unique=True)
    url_destination = models.URLField(max_length=255)
    date_generation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="actif")

    class Meta:
        db_table = "qrcode"

    def __str__(self):
        return f"QR {self.code_unique} -> Table {self.table.numero}"
