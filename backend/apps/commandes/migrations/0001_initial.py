import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("tables", "0004_uuid_unique_and_constraint")]

    operations = [
        migrations.CreateModel(
            name="Commande",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("table", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="commandes", to="tables.table")),
            ],
            options={"db_table": "commande", "ordering": ["-date_creation"]},
        ),
    ]
