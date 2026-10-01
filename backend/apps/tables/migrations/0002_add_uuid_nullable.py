import uuid
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    # Les mêmes colonnes sont déjà créées par 0002_table_qrcode_uuid,
    # migration qui est enregistrée comme appliquée dans cette base.
    dependencies = [('tables', '0002_table_qrcode_uuid')]
    operations = []
