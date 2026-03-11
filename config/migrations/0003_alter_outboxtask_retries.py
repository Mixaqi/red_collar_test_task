from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0002_outboxtask_retries"),
    ]

    operations = [
        migrations.AlterField(
            model_name="outboxtask",
            name="retries",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
