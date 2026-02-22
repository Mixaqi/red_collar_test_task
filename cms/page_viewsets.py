from wagtail.admin.viewsets.pages import PageListingViewSet

from cms.models import MapPage


class MapPageViewSet(PageListingViewSet):
    model = MapPage
    icon = "site"
    menu_label = "Карты"
    add_to_admin_menu = True
    name = "map_pages"


map_viewset = MapPageViewSet("map_pages")
