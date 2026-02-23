from typing import Any

from django.forms import ModelForm
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    add_to_admin_menu = True
    list_display = ["display_coords", "user", "created_at"]

    panels = [
        LeafletPanel("location", heading="Точка"),
        FieldPanel("user", heading="Пользователь"),
    ]

    def get_form_class(self, for_update: bool = False) -> type[ModelForm]:
        form_class: type[ModelForm] = super().get_form_class(for_update=for_update)

        class CustomForm(form_class):  # type: ignore[misc, valid-type]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                if self.instance and self.instance.pk:
                    self.fields["user"].disabled = True

        return CustomForm


class MessageViewSet(SnippetViewSet):
    model = Message
    add_to_admin_menu = True
    list_display = ["text", "point", "user"]

    panels = [
        FieldPanel("point", heading="Точка"),
        FieldPanel("text", heading="Текст"),
        FieldPanel("user", heading="Пользователь"),
    ]
