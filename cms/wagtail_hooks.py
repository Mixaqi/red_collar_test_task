from django.http import HttpRequest
from django.utils.safestring import mark_safe
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


class MapPageViewSet(PageListingViewSet):
    model = MapPage
    icon = "site"
    menu_label = "Карты"
    add_to_admin_menu = True
    name = "map_pages"


map_viewset = MapPageViewSet("map_pages")


@hooks.register("register_admin_viewset")
def register_map_viewset() -> MapPageViewSet:
    return map_viewset


@hooks.register("construct_main_menu")
def hide_unused_buttons(request: HttpRequest, menu_items: list[MenuItem]) -> None:
    menu_items[:] = [
        item
        for item in menu_items
        if item.name not in ["documents", "images", "reports", "help", "settings"]
    ]


@hooks.register("insert_global_admin_css")
def hide_header_elements_css() -> str:
    return mark_safe("""
        <style>
            a[href*="/history/"] {
                display: none !important;
            }

            a[target="_blank"], a[href*="/view/"] {
                display: none !important;
            }
            button[data-side-panel-toggle="status"],
            .w-side-panel-toggle[data-side-panel-toggle="status"] {
                display: none !important;
            }

            [data-side-panel="status"] {
                display: none !important;
            }
        </style>
    """)


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)
