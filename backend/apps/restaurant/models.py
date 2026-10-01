from django.db import models

class Restaurant(models.Model):
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    logo = models.CharField(max_length=255, blank=True)
    banniere = models.CharField(max_length=255, blank=True)
    horaires_ouverture = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "restaurant"

    def __str__(self):
        return self.nom

    @staticmethod
    def instance():
        return Restaurant.objects.first()