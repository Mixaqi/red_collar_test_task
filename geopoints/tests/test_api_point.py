from typing import Any

import pytest
from rest_framework.test import APIClient

from authentication.models import User
from geopoints.models import MapPoint


@pytest.mark.django_db
def test_create_point_success(
    auth_client: APIClient, valid_point_payload: dict[str, Any]
) -> None:
    response = auth_client.post("/api/points/", valid_point_payload, format="json")
    assert response.status_code == 201
    assert response.data["geometry"]["type"] == "Point"


@pytest.mark.django_db
def test_create_point_unauthorized(valid_point_payload: dict[str, Any]) -> None:
    client = APIClient()
    response = client.post("/api/points/", valid_point_payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_point_persists_in_db(
    auth_client: APIClient, valid_point_payload: dict[str, Any], user: User
) -> None:
    response = auth_client.post("/api/points/", valid_point_payload, format="json")
    assert response.status_code == 201
    assert MapPoint.objects.count() == 1
    point = MapPoint.objects.get()
    assert point.user == user


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_payload, expected_code",
    [
        (
            {"location": [1, 2]},
            "not_an_object",
        ),
        (
            {"location": {"type": "MultiPoint", "coordinates": [1, 1]}},
            "invalid_type",
        ),
        (
            {"location": {"type": "NOT_POINT_TYPE", "coordinates": [1, 1]}},
            "invalid_type",
        ),
        (
            {"location": {"type": "Point", "coordinates": ["37.6173", 90.1]}},
            "invalid_coordinates",
        ),
        (
            {"location": {"type": "Point", "coordinates": [90.1, ""]}},
            "invalid_coordinates",
        ),
        ({"location": {"type": "Point"}}, "invalid_format"),
        (
            {
                "location": {
                    "type": "Point",
                    "coordinates": [37.61, 55.75],
                    "crs": {"type": "name", "properties": {"name": "EPSG:3857"}},
                }
            },
            "invalid_srid",
        ),
        ({"location": {"type": "Point", "coordinates": [20, 120]}}, "invalid_latitude"),
        (
            {"location": {"type": "Point", "coordinates": [500, 20]}},
            "invalid_longitude",
        ),
    ],
)
def test_create_invalid_point(
    auth_client: APIClient, invalid_payload: dict[str, Any], expected_code: str
) -> None:
    response = auth_client.post("/api/points/", invalid_payload, format="json")
    assert response.status_code == 400
    assert "location" in response.data
    error_detail = response.data["location"][0]
    assert error_detail.code == expected_code
