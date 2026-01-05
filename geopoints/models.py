from django.contrib.gis.db.models import (
    CASCADE,
    DateTimeField,
    ForeignKey,
    Model,
    PointField,
)
from django.db import models

from authentication.models import User


class MapPoint(Model):
    location: models.Field = PointField(srid=4326)
    user: models.Field = ForeignKey(User, on_delete=CASCADE)
    created_at: models.Field = DateTimeField(auto_now_add=True)
