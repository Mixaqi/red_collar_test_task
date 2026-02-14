from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class MapPage(Page):
    template = "map_page.html"
    description = RichTextField(blank=True)
    points = ParentalManyToManyField(
        "geopoints.MapPoint", blank=True, related_name="pages"
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("points"),
    ]
