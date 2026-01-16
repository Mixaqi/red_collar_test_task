import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("geopoints", "0002_alter_mappoint_user_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mappoint",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                srid=4326, unique=True
            ),
        ),
    ]
