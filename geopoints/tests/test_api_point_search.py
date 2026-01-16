import pytest
from rest_framework.test import APIClient

from geopoints.models import MapPoint
from geopoints.tests.conftest import POINT_SEARCH_URL


@pytest.mark.django_db
def test_point_search_unauthorized(point_search_valid_params: dict[str, float]) -> None:
    client = APIClient()
    response = client.get(POINT_SEARCH_URL, point_search_valid_params)
    assert response.status_code == 401


@pytest.mark.django_db
def test_point_search_missing_params(auth_client: APIClient) -> None:
    response = auth_client.get(POINT_SEARCH_URL)
    assert response.status_code == 400


@pytest.mark.django_db
def test_point_search_success(
    auth_client: APIClient,
    map_points: MapPoint,
    point_search_valid_params: dict[str, float],
) -> None:
    response = auth_client.get(POINT_SEARCH_URL, point_search_valid_params)

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]["features"]) == 2
