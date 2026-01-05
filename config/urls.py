from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path(
                    "auth/", include("authentication.urls", namespace="authentication")
                ),
                path("points/", include("geopoints.urls", namespace="geopoints")),
            ]
        ),
    ),
]
