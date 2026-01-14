from typing import Any

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User


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
def valid_point_payload() -> dict[str, Any]:
    return {"location": {"type": "Point", "coordinates": [37.6173, 55.7558]}}
