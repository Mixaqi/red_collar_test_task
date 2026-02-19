from django.contrib import admin
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "api/",
        include(
            [
                path(
                    "auth/",
                    include(
                        ("authentication.urls", "authentication"),
                        namespace="authentication",
                    ),
                ),
                path(
                    "points/",
                    include(("geopoints.urls", "geopoints"), namespace="geopoints"),
                ),
            ]
        ),
    ),
    re_path(r"", include(wagtail_urls)),
]
