from typing import Any, cast

from django.db import IntegrityError, transaction
from rest_framework.serializers import (
    FloatField,
    PrimaryKeyRelatedField,
    Serializer,
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer

from geopoints.exceptions import PointAlreadyExistsError
from geopoints.fields import SafePointField
from geopoints.models import MapPoint, Message


class MapPointSerializer(GeoFeatureModelSerializer):
    location = SafePointField()

    class Meta:
        model = MapPoint
        geo_field = "location"
        fields = ("location", "created_at")

    def create(self, validated_data: dict[str, Any]) -> MapPoint:
        try:
            with transaction.atomic():
                validated_data["user"] = self.context["request"].user
                return cast(MapPoint, super().create(validated_data))
        except IntegrityError as e:
            raise PointAlreadyExistsError() from e


class MessageSerializer(ModelSerializer):
    point = PrimaryKeyRelatedField(queryset=MapPoint.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ["point", "text"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data: dict[str, Any]) -> Message:
        user = self.context["request"].user
        return Message.objects.create(user=user, **validated_data)


class PointSearchSerializer(Serializer):
    latitude = FloatField(min_value=-90, max_value=90)
    longitude = FloatField(min_value=-180, max_value=180)
    radius = FloatField(min_value=0)
