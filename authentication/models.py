from typing import Any, cast

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, EmailField


class UserManager(BaseUserManager):
    def create_user(
        self, username: str, email: str, password: str, **extra_fields: Any
    ) -> User:
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = cast(User, self.model(username=username, email=email, **extra_fields))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields: Any
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username: CharField = CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )
    email: EmailField = EmailField(unique=True, verbose_name="Электронная почта")
    is_staff: BooleanField = BooleanField(default=False, verbose_name="Персонал")
    is_active: BooleanField = BooleanField(default=True, verbose_name="Активен")
    date_joined: DateTimeField = DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    USERNAME_FIELD: str = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.username)
