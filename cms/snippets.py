from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    add_to_admin_menu = True
    list_display = ["__str__", "user", "created_at"]

    panels = [
        LeafletPanel("location", heading="Точка"),
        FieldPanel("user", heading="Пользователь", read_only=True),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    add_to_admin_menu = True
    list_display = ["text", "point", "user"]

    panels = [
        FieldPanel("point", heading="Точка"),
        FieldPanel("text", heading="Текст"),
        FieldPanel("user", heading="Пользователь"),
    ]
