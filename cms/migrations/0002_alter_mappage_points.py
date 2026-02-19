import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
        ("geopoints", "0003_alter_mappoint_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mappage",
            name="points",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, related_name="pages", to="geopoints.mappoint"
            ),
        ),
    ]
