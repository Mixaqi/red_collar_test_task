from django.urls import path

from geopoints.views import MessageCreateView, PointCreateView, PointSearchView


app_name = "geopoints"
urlpatterns = [
    path("", PointCreateView.as_view(), name="point-create"),
    path("message/", MessageCreateView().as_view(), name="message-create"),
    path("search/", PointSearchView.as_view(), name="points-search"),
]
