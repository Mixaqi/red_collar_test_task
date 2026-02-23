from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from config.mixins import DisableUserFieldMixin
from geopoints.models import MapPoint, Message


class MapPointViewSet(DisableUserFieldMixin, SnippetViewSet):
    model = MapPoint
    add_to_admin_menu = True
    list_display = ["display_coords", "user", "created_at"]

    panels = [
        LeafletPanel("location", heading="Точка"),
        FieldPanel("user", heading="Пользователь"),
    ]


class MessageViewSet(DisableUserFieldMixin, SnippetViewSet):
    model = Message
    add_to_admin_menu = True
    list_display = ["text", "point", "user"]

    panels = [
        FieldPanel("point", heading="Точка"),
        FieldPanel("text", heading="Текст"),
        FieldPanel("user", heading="Пользователь"),
    ]
