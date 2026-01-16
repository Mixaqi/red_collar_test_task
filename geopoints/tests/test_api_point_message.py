from typing import Any

import pytest
from rest_framework.test import APIClient

from geopoints.tests.conftest import MESSAGE_CREATE_URL


@pytest.mark.django_db
def test_message_create_unauthorized(message_payload: dict[str, Any]) -> None:
    client = APIClient()

    response = client.post(
        MESSAGE_CREATE_URL,
        message_payload,
        format="json",
    )

    assert response.status_code == 401
