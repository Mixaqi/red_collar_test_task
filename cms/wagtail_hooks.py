from rest_framework.request import Request
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailgeowidget.panels import LeafletPanel

from cms.models import MapPage
from geopoints.models import MapPoint, Message


class MapPointViewSet(SnippetViewSet):
    model = MapPoint
    add_to_admin_menu = True
    list_display = ["__str__", "user", "created_at"]

    panels: list[LeafletPanel | FieldPanel] = [
        LeafletPanel("location", heading="Точка"),
        FieldPanel("user", heading="Пользователь"),
    ]


class MessageViewSet(SnippetViewSet):
    model = Message
    add_to_admin_menu = True
    list_display = ["text", "point", "user"]
    panels: list[FieldPanel] = [
        FieldPanel("point", heading="Точка"),
        FieldPanel("text", heading="Текст"),
        FieldPanel("user", heading="Пользователь"),
    ]


class MapPageViewSet(PageListingViewSet):
    model: type[MapPage] = MapPage
    icon: str = "site"
    menu_label: str = "Карты"
    menu_order: int = 100
    add_to_admin_menu: bool = True
    name: str = "map_pages"


map_viewset: MapPageViewSet = MapPageViewSet("map_pages")


@hooks.register("register_admin_viewset")
def register_map_viewset() -> PageListingViewSet:
    return map_viewset


@hooks.register("construct_main_menu")
def hide_unused_buttons(request: Request, hidden_menu_items: list[MenuItem]) -> None:
    hidden_menu_items[:] = [
        item
        for item in hidden_menu_items
        if item.name not in ["documents", "images", "reports", "help", "settings"]
    ]


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
