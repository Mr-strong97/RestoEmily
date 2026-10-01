from django.db import migrations

CATEGORIES_INITIALES = ["Boissons", "Plan National", "Plan International"]

def creer_categories(apps, schema_editor):
    Categorie = apps.get_model('menu', 'Categorie')
    Restaurant = apps.get_model('restaurant', 'Restaurant')
    restaurant = Restaurant.objects.first()
    for ordre, nom in enumerate(CATEGORIES_INITIALES, start=1):
        Categorie.objects.get_or_create(nom=nom, restaurant=restaurant, defaults={"ordre_affichage": ordre})

def supprimer_categories(apps, schema_editor):
    Categorie = apps.get_model('menu', 'Categorie')
    Categorie.objects.filter(nom__in=CATEGORIES_INITIALES, produits__isnull=True).delete()

class Migration(migrations.Migration):
    dependencies = [('menu', '0001_initial'), ('restaurant', '0001_initial')]
    operations = [migrations.RunPython(creer_categories, supprimer_categories)]