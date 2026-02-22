from django.contrib.gis.db.models import (
    CASCADE,
    SET_NULL,
    DateTimeField,
    ForeignKey,
    Model,
    PointField,
    TextField,
)

from authentication.models import User


class MapPoint(Model):
    location = PointField(srid=4326, unique=True, verbose_name=("Локация"))
    user = ForeignKey(
        User, on_delete=SET_NULL, null=True, blank=True, verbose_name="Пользователь"
    )
    created_at: DateTimeField = DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Точка на карте"
        verbose_name_plural = "Точки на карте"

    @property
    def display_coords(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Точка [{self.location.y:.4f}, {self.location.x:.4f}]"


class Message(Model):
    point = ForeignKey(
        MapPoint, on_delete=CASCADE, related_name="messages", verbose_name="Точка"
    )
    text: TextField = TextField(verbose_name="Текст")
    user = ForeignKey(
        User, on_delete=SET_NULL, null=True, blank=True, verbose_name="Пользователь"
    )
    created_at: DateTimeField = DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self) -> str:
        if self.user:
            username = self.user.username
        else:
            username = "Удаленный пользователь"
        return f"От пользователя {username} для точки ({self.point.location.x}, {self.point.location.y}) {self.text[:20]}..."
