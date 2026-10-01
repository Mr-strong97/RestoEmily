import apps.administrateurs.models
import django.db.models.deletion
from django.db import migrations, models


def remapper_anciennes_valeurs(apps, schema_editor):
    Administrateur = apps.get_model('administrateurs', 'Administrateur')
    Administrateur.objects.filter(role='admin').update(role='personnel')
    Administrateur.objects.filter(statut='en_attente').update(statut='inactif')


class Migration(migrations.Migration):
    dependencies = [
        ('administrateurs', '0003_administrateur_id_uuid'),
        ('restaurant', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='administrateur', name='restaurant',
            field=models.ForeignKey(default=apps.administrateurs.models._restaurant_par_defaut,
                on_delete=django.db.models.deletion.PROTECT, related_name='administrateurs', to='restaurant.restaurant'),
        ),
        migrations.RunPython(remapper_anciennes_valeurs, migrations.RunPython.noop),
        migrations.AlterField(model_name='administrateur', name='role',
            field=models.CharField(choices=[('super_admin', 'Super Administrateur'), ('gerant', 'Gérant'), ('personnel', 'Personnel')], default='personnel', max_length=30)),
        migrations.AlterField(model_name='administrateur', name='statut',
            field=models.CharField(choices=[('actif', 'Actif'), ('inactif', 'Inactif')], default='inactif', max_length=20)),
    ]
