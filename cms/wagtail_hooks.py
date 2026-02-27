from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.html import format_html_join
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet

from cms.page_viewsets import MapPageViewSet, map_viewset
from cms.snippets import MapPointViewSet, MessageViewSet


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)

ADMIN_CSS_FILES: list[str] = ["hide_status.css", "hide_header_elements.css"]


@hooks.register("register_admin_viewset")
def register_map_viewset() -> MapPageViewSet:
    return map_viewset


@hooks.register("construct_main_menu")
def hide_unused_buttons(request: HttpRequest, menu_items: list[MenuItem]) -> None:
    menu_items[:] = [
        item
        for item in menu_items
        if item.name
        not in ["documents", "images", "reports", "help", "settings", "explorer"]
    ]


@hooks.register("insert_global_admin_css")
def insert_admin_css() -> str:
    return format_html_join(
        "\n",
        '<link rel="stylesheet" href="{}">',
        ((static(path),) for path in ADMIN_CSS_FILES),
    )
