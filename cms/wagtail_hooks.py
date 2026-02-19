from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    list_display = ["__str__", "user", "created_at"]

    panels: list[LeafletPanel | FieldPanel] = [
        LeafletPanel("location", heading=_("Точка")),
        FieldPanel("user", heading=_("Пользователь")),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    list_display = ["text", "point", "user"]
    panels: list[FieldPanel] = [
        FieldPanel("point", heading=_("Точка")),
        FieldPanel("text", heading=_("Текст")),
        FieldPanel("user", heading=_("Пользователь")),
    ]


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
