from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    list_display = ["location", "user", "created_at"]
    list_display_labels = {
        "location": _("Локация"),
        "user": _("Пользователь"),
        "created_at": _("Дата создания"),
    }

    panels: list[LeafletPanel | FieldPanel] = [
        LeafletPanel("location", heading=_("Точка")),
        FieldPanel("user", heading=_("Пользователь")),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    list_display = ["text", "point", "user"]
    list_display_labels = {
        "text": _("Текст"),
        "user": _("Пользователь"),
        "created_at": _("Дата создания"),
    }
    panels: list[FieldPanel] = [
        FieldPanel("point", heading=_("Точка")),
        FieldPanel("text", heading=_("Текст")),
        FieldPanel("user", heading=_("Пользователь")),
    ]


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
