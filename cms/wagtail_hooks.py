from rest_framework.request import Request
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from geopoints.models import MapPoint, Message


@hooks.register("construct_main_menu")
def hide_unused_buttons(request: Request, menu_items: list[MenuItem]) -> None:
    menu_items[:] = [
        item
        for item in menu_items
        if item.name not in ["documents", "images", "reports", "help", "settings"]
    ]


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    list_display = ["__str__", "user", "created_at"]

    panels: list[LeafletPanel | FieldPanel] = [
        LeafletPanel("location", heading="Точка"),
        FieldPanel("user", heading="Пользователь"),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    list_display = ["text", "point", "user"]
    panels: list[FieldPanel] = [
        FieldPanel("point", heading="Точка"),
        FieldPanel("text", heading="Текст"),
        FieldPanel("user", heading="Пользователь"),
    ]


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
