from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("administrateurs", "0005_restaurant_fk_et_remap_valeurs")]

    operations = [
        migrations.AlterField(
            model_name="administrateur",
            name="email",
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]
