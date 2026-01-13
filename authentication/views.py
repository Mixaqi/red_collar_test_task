from typing import Any, cast

from django.contrib.auth.models import update_last_login
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.serializers import RegisterSerializer
from authentication.models import User


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]  # type: ignore[assignment]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = cast(
            TokenObtainPairSerializer,
            self.get_serializer(data=request.data),
        )

        serializer.is_valid(raise_exception=True)
        if serializer.user is None:
            raise AuthenticationFailed("Invalid Credentials")
        update_last_login(User, serializer.user)
        return Response(serializer.validated_data)


class MeView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = cast(User, request.user)

        return Response(
            {
                "id": user.pk,
                "username": user.username,
            }
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        refresh: str | None = request.data.get("refresh")

        if refresh is None:
            raise ValidationError("refresh token required")

        token = RefreshToken(cast(Any, refresh))
        token.blacklist()
        return Response({"detail": "Logged out"})
