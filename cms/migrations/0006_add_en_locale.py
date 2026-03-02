from typing import Any, ClassVar

from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps


def create_en_locale(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Locale: Any = apps.get_model("wagtailcore", "Locale")
    Locale.objects.get_or_create(language_code="en")


class Migration(migrations.Migration):
    dependencies: ClassVar[list[tuple[str, str]]] = [
        ("cms", "0005_alter_mappage_options_alter_mappagepoint_options_and_more"),
        ("wagtailcore", "0001_initial"),
    ]
    operations: ClassVar[list[migrations.operations.base.Operation]] = [
        migrations.RunPython(create_en_locale, migrations.RunPython.noop),
    ]
