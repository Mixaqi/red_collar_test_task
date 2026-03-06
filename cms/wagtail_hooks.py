from django.db import transaction
from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.html import format_html_join
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from cms.page_viewsets import MapPageViewSet, map_viewset
from cms.snippets import MapPointViewSet, MessageViewSet
from cms.tasks import send_telegram_message
from config.models import OutboxStatus, OutboxTask


register_snippet(MapPointViewSet)
register_snippet(MessageViewSet)

ADMIN_CSS_FILES: list[str] = ["hide_status.css", "hide_header_elements.css"]


@hooks.register("register_admin_viewset")
def register_map_viewset() -> MapPageViewSet:
    """Register the custom map viewset in the Wagtail admin.

    Returns:
        MapPageViewSet: The viewset class used by Wagtail admin to manage map pages.
    """
    return map_viewset


@hooks.register("construct_main_menu")
def hide_unused_buttons(request: HttpRequest, menu_items: list[MenuItem]) -> None:
    """Remove unused buttons from the main Wagtail admin menu.

    Args:
        request (HttpRequest): The current request object
        menu_items (list[MenuItem]): List of existing menu items, which will be modified
        in-place.
    """

    menu_items[:] = [
        item
        for item in menu_items
        if item.name
        not in ["documents", "images", "reports", "help", "settings", "explorer"]
    ]


@hooks.register("insert_global_admin_css")
def insert_admin_css() -> str:
    """Insert global CSS files into the Wagtail admin.

    Returns:
        str: HTML <link> tags for each CSS file specified in ADMIN_CSS_FILES.
    """
    return format_html_join(
        "\n",
        '<link rel="stylesheet" href="{}">',
        ((static(path),) for path in ADMIN_CSS_FILES),
    )


@hooks.register("after_edit_page")
def create_outbox_task(request: HttpRequest, page: Page) -> None:
    outbox = OutboxTask.objects.create(
        task_name="send_telegram_message",
        payload={"page_id": page.id, "title": page.title},
        status=OutboxStatus.PENDING,
    )
    transaction.on_commit(lambda: send_telegram_message.delay(outbox.id))
