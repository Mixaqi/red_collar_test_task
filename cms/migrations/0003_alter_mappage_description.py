import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0002_alter_mappage_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mappage",
            name="description",
            field=wagtail.fields.StreamField(
                [("paragraph", 0)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {"label": "text"})
                },
            ),
        ),
    ]
