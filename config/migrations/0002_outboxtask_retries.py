from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="outboxtask",
            name="retries",
            field=models.IntegerField(default=0),
        ),
    ]
