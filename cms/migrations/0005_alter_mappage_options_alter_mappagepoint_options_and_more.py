import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0004_alter_mappage_options_remove_mappage_points_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mappage",
            options={
                "verbose_name": "Страница с картой",
                "verbose_name_plural": "Страницы с картой",
            },
        ),
        migrations.AlterModelOptions(
            name="mappagepoint",
            options={
                "verbose_name": "Точка на странице",
                "verbose_name_plural": "Точки на странице",
            },
        ),
        migrations.AlterField(
            model_name="mappage",
            name="description",
            field=wagtail.fields.StreamField(
                [("paragraph", 0)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {"label": "Текст"})
                },
            ),
        ),
    ]
