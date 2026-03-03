from typing import Any, ClassVar

from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps


def remove_welcome_page(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    Page: Any = apps.get_model("wagtailcore", "Page")
    welcome_page: Any = Page.objects.filter(depth=2).first()

    if welcome_page:
        welcome_page.delete()


class Migration(migrations.Migration):
    dependencies: ClassVar[list[tuple[str, str]]] = [
        ("cms", "0006_add_en_locale"),
    ]

    operations: ClassVar[list[migrations.operations.base.Operation]] = [
        migrations.RunPython(remove_welcome_page, migrations.RunPython.noop)
    ]
