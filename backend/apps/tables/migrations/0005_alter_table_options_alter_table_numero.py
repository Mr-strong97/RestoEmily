import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tables", "0004_uuid_unique_and_constraint")]

    operations = [
        migrations.AlterModelOptions(name="table", options={"ordering": ["numero"]}),
        migrations.AlterField(
            model_name="table",
            name="numero",
            field=models.PositiveSmallIntegerField(
                unique=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
    ]
