import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_point_success(auth_client: APIClient) -> None:
    payload = {
        "location": {
            "type": "Point",
            "coordinates": [37.6173, 55.7558],
        }
    }
    response = auth_client.post("/api/points/", payload, format="json")
    assert response.status_code == 201
    assert response.data["geometry"]["type"] == "Point"
