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
    location = PointField(srid=4326, unique=True)
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    created_at: DateTimeField = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Point {self.pk} at {self.location}"


class Message(Model):
    point = ForeignKey(MapPoint, on_delete=CASCADE, related_name="messages")
    text: TextField = TextField()
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    created_at: DateTimeField = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.user:
            username = self.user.username
        else:
            "Deleted User"
        return f"By {username} for point #{self.point.pk}: {self.text[:20]}..."
