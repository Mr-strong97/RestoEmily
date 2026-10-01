import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


def _restaurant_par_defaut():
    from django.db.utils import OperationalError, ProgrammingError
    try:
        from apps.restaurant.models import Restaurant
        r = Restaurant.objects.first()
        return r.pk if r else None
    except (OperationalError, ProgrammingError):
        return None


class AdministrateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "super_admin")
        extra_fields.setdefault("statut", "actif")
        return self.create_user(email, password, **extra_fields)


class Administrateur(AbstractBaseUser):
    ROLE_CHOICES = [
        ("super_admin", "Super Administrateur"),
        ("gerant", "Gérant"),
        ("personnel", "Personnel"),
    ]
    STATUT_CHOICES = [
        ("actif", "Actif"),
        ("inactif", "Inactif"),
        ("bloque", "Bloqué"),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="personnel")
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="inactif")
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.PROTECT, related_name="administrateurs",
        default=_restaurant_par_defaut,
    )

    objects = AdministrateurManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "prenom"]

    class Meta:
        db_table = "administrateur"

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"

    @property
    def is_active(self):
        return self.statut == "actif"

    @property
    def is_staff(self):
        return self.role in ("super_admin", "gerant", "personnel")

    def has_perm(self, perm, obj=None):
        return self.role == "super_admin"

    def has_module_perms(self, app_label):
        return self.role == "super_admin"
