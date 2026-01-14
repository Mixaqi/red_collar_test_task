from typing import Any

import pytest
from rest_framework.test import APIClient


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
