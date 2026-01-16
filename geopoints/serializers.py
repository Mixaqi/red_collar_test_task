from typing import Any, cast

from django.db import IntegrityError, transaction
from rest_framework.exceptions import NotFound
from rest_framework.serializers import (
    FloatField,
    Serializer,
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer

from geopoints.exceptions import PointAlreadyExistsError
from geopoints.fields import SafePointField
from geopoints.models import MapPoint, Message
from geopoints.utils import get_map_point


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
    location = SafePointField(write_only=True)

    class Meta:
        model = Message
        fields = ["text", "location", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data: dict[str, Any]) -> Message:
        point_geom = validated_data.pop("location")
        map_point = get_map_point(point_geom)
        if not map_point:
            raise NotFound("No MapPoint found for these coordinates")
        user = self.context["request"].user
        message = Message.objects.create(point=map_point, user=user, **validated_data)
        return message

    def to_representation(self, instance: Any) -> Any:
        return_value = super().to_representation(instance)
        if instance.point:
            return_value["location"] = {
                "type": "Point",
                "coordinates": [instance.point.location.x, instance.point.location.y],
            }
        return return_value


class PointSearchSerializer(Serializer):
    latitude = FloatField(min_value=-90, max_value=90)
    longitude = FloatField(min_value=-180, max_value=180)
    radius = FloatField(min_value=0)
