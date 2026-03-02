from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator

from authentication.models import User


class RegisterSerializer(ModelSerializer):
    """Serializer for user registration

    Handles validation and creation of new user with unique username and email.
    Password is validated using Django's built-in password validators.

    Attributes:
        username (CharField): Unique username of the user.
        email (EmailField): Unique email address of the user.
        password (CharField): User password (write-only).
    """

    username = CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_password(self, value: str) -> str:
        """Validate the password using DRF validate_ system. Checks for 8+ symbols.

        Args:
            value (str): Raw password string

        Raises:
            ValidationError: if the password does not satisfy validation rules

        Returns:
            str: Validated password
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError from e
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create a new user instance

        Args:
            validated_data (dict[str, Any]): Validated serializer data.

        Raises:
            ValidationError: if a user with the same username or email already exists

        Returns:
            User: Created user instance
        """
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError as e:
            raise ValidationError(
                {"detail": "User with this username or email already exists"}
            ) from e
