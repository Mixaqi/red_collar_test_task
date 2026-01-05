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
    username = CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError from e
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError as e:
            raise ValidationError(
                {"detail": "User with this username or email already exists"}
            ) from e
