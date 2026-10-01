import apps.tables.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def remapper_anciennes_valeurs(apps, schema_editor):
    Table = apps.get_model('tables', 'Table')
    QRCode = apps.get_model('tables', 'QRCode')
    Table.objects.filter(statut='inactive').update(statut='libre')
    QRCode.objects.filter(statut__in=['expire', 'desactive']).update(statut='inactif')


class Migration(migrations.Migration):
    dependencies = [('restaurant', '0001_initial'), ('tables', '0005_alter_table_options_alter_table_numero')]
    operations = [
        migrations.AddField(model_name='table', name='restaurant',
            field=models.ForeignKey(default=apps.tables.models._restaurant_par_defaut, on_delete=django.db.models.deletion.PROTECT, related_name='tables', to='restaurant.restaurant')),
        migrations.RunPython(remapper_anciennes_valeurs, migrations.RunPython.noop),
        migrations.AlterField(model_name='qrcode', name='statut',
            field=models.CharField(choices=[('actif', 'Actif'), ('inactif', 'Inactif')], default='actif', max_length=20)),
        migrations.AlterField(model_name='qrcode', name='url_destination', field=models.URLField(max_length=255)),
        migrations.AlterField(model_name='table', name='numero',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
        migrations.AlterField(model_name='table', name='statut',
            field=models.CharField(choices=[('libre', 'Libre'), ('occupee', 'Occupée')], default='libre', max_length=20)),
        migrations.AddConstraint(model_name='table', constraint=models.UniqueConstraint(fields=('numero', 'restaurant'), name='numero_unique_par_restaurant')),
    ]
