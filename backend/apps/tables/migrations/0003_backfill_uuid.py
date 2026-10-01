import uuid
from django.db import migrations

def generer_uuid_par_ligne(apps, schema_editor):
    Table = apps.get_model('tables', 'Table')
    QRCode = apps.get_model('tables', 'QRCode')
    for t in Table.objects.all():
        t.uuid = uuid.uuid4(); t.save(update_fields=['uuid'])
    for q in QRCode.objects.all():
        q.uuid = uuid.uuid4(); q.save(update_fields=['uuid'])

class Migration(migrations.Migration):
    dependencies = [('tables', '0002_add_uuid_nullable')]
    operations = [migrations.RunPython(generer_uuid_par_ligne, migrations.RunPython.noop)]