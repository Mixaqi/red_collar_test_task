from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    list_display = ["location", "user", "created_at"]

    panels: list[LeafletPanel | FieldPanel] = [
        LeafletPanel("location"),
        FieldPanel("user"),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    list_display = ["text", "point", "user"]

    panels: list[FieldPanel] = [
        FieldPanel("point"),
        FieldPanel("text"),
        FieldPanel("user"),
    ]


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
