from django.urls import include, path

from geopoints.views import (
    MessageCreateView,
    MessageSearchView,
    PointCreateView,
    PointSearchView,
)


app_name = "geopoints"
urlpatterns = [
    path("", PointCreateView.as_view(), name="point-create"),
    path("search/", PointSearchView.as_view(), name="points-search"),
    path(
        "message/",
        include(
            [
                path("", MessageCreateView.as_view(), name="message-create"),
                path("search/", MessageSearchView.as_view(), name="message-search"),
            ]
        ),
    ),
]
