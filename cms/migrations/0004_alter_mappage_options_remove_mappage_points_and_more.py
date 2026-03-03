import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0003_alter_mappage_description"),
        ("geopoints", "0004_alter_mappoint_options_alter_message_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mappage",
            options={
                "verbose_name": "Страница с картой",
                "verbose_name_plural": "Страницы с картами",
            },
        ),
        migrations.RemoveField(
            model_name="mappage",
            name="points",
        ),
        migrations.AlterField(
            model_name="mappage",
            name="description",
            field=wagtail.fields.StreamField(
                [("paragraph", 0)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {"label": "текст"})
                },
            ),
        ),
        migrations.CreateModel(
            name="MapPagePoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="map_points",
                        to="cms.mappage",
                    ),
                ),
                (
                    "point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="geopoints.mappoint",
                    ),
                ),
            ],
            options={
                "verbose_name": "Точка страницы",
                "verbose_name_plural": "Точки страницы",
            },
        ),
    ]
