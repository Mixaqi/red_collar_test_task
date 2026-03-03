from wagtail.admin.viewsets.pages import PageListingViewSet

from cms.models import MapPage


class MapPageViewSet(PageListingViewSet):
    """Admin viewset for listing and managing MapPage instances.

    Registers a custom page listing in the Wagtail admin under
    a separate menu section labeled "Карты".
    """

    model = MapPage
    icon = "site"
    menu_label = "Карты"
    add_to_admin_menu = True
    name = "map_pages"


map_viewset = MapPageViewSet("map_pages")
