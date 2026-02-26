from django.forms import CharField
from wagtail.admin.forms.auth import LoginForm


class CustomLoginForm(LoginForm):
    password = CharField(required=True, label="Пароль")
