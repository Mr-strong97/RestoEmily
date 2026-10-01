import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('tables', '0003_backfill_uuid')]
    operations = [
        migrations.AlterField(model_name='table', name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
        migrations.AlterField(model_name='qrcode', name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
    ]
