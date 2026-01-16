from typing import Any

import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from geopoints.models import MapPoint


POINT_SEARCH_URL = "/api/points/search/"
POINT_CREATION_URL = "/api/points/"
MESSAGE_CREATE_URL = "/api/points/message/"


@pytest.fixture
def user(db: Any) -> User:
    return User.objects.create_user(
        username="testuser", password="testpassword123", email="test@mail.com"
    )


@pytest.fixture
def auth_client(user: User) -> APIClient:
    client = APIClient()

    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def map_point(user: User) -> MapPoint:
    return MapPoint.objects.create(user=user, location=Point(37.61, 55.75, srid=4326))


@pytest.fixture
def map_points(user: User) -> list[MapPoint]:
    return [
        MapPoint.objects.create(
            user=user,
            location=Point(37.61, 55.75, srid=4326),
        ),
        MapPoint.objects.create(
            user=user,
            location=Point(37.62, 55.76, srid=4326),
        ),
        MapPoint.objects.create(
            user=user,
            location=Point(30.31, 59.93, srid=4326),
        ),
    ]


@pytest.fixture
def point_search_valid_params() -> dict[str, float]:
    return {
        "latitude": 55.75,
        "longitude": 37.61,
        "radius": 5,
        "offset": 0,
    }


@pytest.fixture
def message_payload(valid_point_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "text": "FAWFAWKFMAWKF",
        "location": valid_point_payload,
    }


@pytest.fixture
def valid_point_payload() -> dict[str, Any]:
    return {"location": {"type": "Point", "coordinates": [37.6173, 55.7558]}}
