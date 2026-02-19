from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Page


class MapPage(Page):
    template = "map_page.html"
    description = StreamField(
        [
            ("paragraph", RichTextBlock(label="text")),
        ],
        blank=True,
    )
    points = ParentalManyToManyField(
        "geopoints.MapPoint", blank=True, related_name="pages"
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", heading="Описание"),
        FieldPanel("points", heading="Точки"),
    ]
