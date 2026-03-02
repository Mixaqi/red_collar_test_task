from django.contrib.admin import display
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
    """Represents a point on the map associated with a user.

    Attributes:
        location (PointField): Geographic location of the point (SRID 4326), unique.
        user (ForeignKey[User]): User who created the point. Can be null if deleted.
        created_at (DateTimeField): Timestamp when the point was created.

    Methods:
        display_coords() -> str:
            Returns a string representation of the point's coordinates for admin display.
    """

    location = PointField(srid=4326, unique=True, verbose_name=("Локация"))
    user = ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name="Пользователь")
    created_at: DateTimeField = DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Точка на карте "
        verbose_name_plural = "Точки на карте "

    @display(description="Координаты")
    def display_coords(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Точка [{self.location.y:.4f}, {self.location.x:.4f}]"


class Message(Model):
    """Represents a message attached to a MapPoint.

    Attributes:
        point (ForeignKey[MapPoint]): The map point this message is associated with
        text (TextField): The message content
        user (ForeignKey[User]):The user who created the message.Can be null if deleted
        created_at (DateTimeField): Timestamp when the message was created
    """

    point = ForeignKey(
        MapPoint, on_delete=CASCADE, related_name="messages", verbose_name="Точка"
    )
    text: TextField = TextField(verbose_name="Текст")
    user = ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name="Пользователь")
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
