from django.urls import path

from geopoints.views import MessageCreateView, PointCreateView


app_name = "geopoints"
urlpatterns = [
    path("", PointCreateView.as_view(), name="point-create"),
    path("message/", MessageCreateView().as_view(), name="message-create"),
]
