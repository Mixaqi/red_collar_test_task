from django.urls import path

from geopoints.views import PointCreateView


app_name = "geopoints"
urlpatterns = [
    path("", PointCreateView.as_view(), name="point-create"),
]
