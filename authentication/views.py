from typing import Any, cast

from django.contrib.auth.models import update_last_login
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from authentication.models import User
from authentication.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """API View for user registration.
    Allows unauthenticated users to create a new account.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """API endpoint for user authentication.

    Returns JWT access and refresh tokens if credentials are valid.
    Updates the user's last login timestamp
    """

    permission_classes = [permissions.AllowAny]  # type: ignore[assignment]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Authenticate user and return JWT token pair

        Args:
            request (Request): Incoming HTTP request containing credentials

        Raises:
            AuthenticationFailed: If authentication fails

        Returns:
            Response: JSON response containing access and refresh tokens
        """

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
    """API View to get info about the current authenticated user"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Return basic information about the current user

        Args:
            request (Request): Authenticated (Bearer <access token> in header) request

        Returns:
            Response: JSON containing user id and username
        """
        user = cast(User, request.user)

        return Response(
            {
                "id": user.pk,
                "username": user.username,
            }
        )


class LogoutView(APIView):
    """API View for logout a user.

    Blacklists the provided refresh token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Invalidate the provided refresh token.

        Args:
            request (Request): Authenticated (Bearer <access token> in header)
            request containing refresh token

        Raises:
            ValidationError: If refresh token is not provided.

        Returns:
            Response: Confirmation message
        """
        refresh: str | None = request.data.get("refresh")

        if refresh is None:
            raise ValidationError("refresh token required")

        token = RefreshToken(cast(Any, refresh))
        token.blacklist()
        return Response({"detail": "Logged out"})
