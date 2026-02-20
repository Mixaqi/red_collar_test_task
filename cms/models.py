from typing import TYPE_CHECKING

from django.db.models import CASCADE, ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page


if TYPE_CHECKING:
    from geopoints.models import MapPoint


class MapPage(Page):
    template = "map_page.html"

    description = StreamField(
        [
            ("paragraph", RichTextBlock(label="текст")),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", heading="Описание"),
        InlinePanel("map_points", label="Точки"),
    ]

    class Meta:
        verbose_name = "Страница с картой"
        verbose_name_plural = "Страницы с картами"


class MapPagePoint(Orderable):
    page = ParentalKey(
        "cms.MapPage",
        on_delete=CASCADE,
        related_name="map_points",
    )

    point: ForeignKey[MapPoint] = ForeignKey(
        "geopoints.MapPoint",
        on_delete=CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("point"),
    ]

    class Meta:
        verbose_name = "Точка страницы"
        verbose_name_plural = "Точки страницы"
