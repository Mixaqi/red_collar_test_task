from django.http import HttpRequest
from django.utils.safestring import mark_safe
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet

from cms.page_viewsets import MapPageViewSet, map_viewset
from cms.snippets import MapPointViewSet, MessageViewSet


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)


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

            th a[href*="ordering=content_type__model"] {
                display: none !important;
            }
        </style>
    """)
