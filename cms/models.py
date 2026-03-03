from typing import TYPE_CHECKING

from django.db.models import CASCADE, ForeignKey
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page


if TYPE_CHECKING:
    from geopoints.models import MapPoint


class MapPage(Page):
    """Page model that displays a map with related map points.

    Provides a rich-text description block and allows attaching
    multiple MapPoint objects via an inline relationship. Links with
    map_page.html template
    """

    template = "map_page.html"
    parent_page_types = ["wagtailcore.Page"]

    description = StreamField(
        [
            ("paragraph", RichTextBlock(label=_("Текст"))),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description", heading=_("Сообщение")),
        InlinePanel("map_points", label=f"{_('Точки')}"),
    ]

    class Meta:
        verbose_name = _("Страница с картой")
        verbose_name_plural = _("Страницы с картой")


class MapPagePoint(Orderable):
    """Intermediate model linking MapPage with MapPoint."""

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
        verbose_name = _("Точка на странице")
        verbose_name_plural = _("Точки на странице")
