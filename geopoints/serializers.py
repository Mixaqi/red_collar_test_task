from typing import Any, cast

from django.contrib.gis.geos import GEOSGeometry, Point
from rest_framework.serializers import PrimaryKeyRelatedField, ValidationError
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer

from geopoints.models import MapPoint, Message


class MapPointSerializer(GeoFeatureModelSerializer):
    location = GeometryField()

    class Meta:
        model = MapPoint
        geo_field = "location"
        fields = ("location", "created_at")

    def validate_location(self, geo_value: GEOSGeometry) -> GEOSGeometry:
        if geo_value.hasz:
            raise ValidationError(
                "Only 2D coordinates (longtitude and latitude) are allowed"
            )
        if not isinstance(geo_value, Point):
            raise ValidationError(f"Use type Point instead of {geo_value.geom_type}.")
        return geo_value

    def create(self, validated_data: dict[str, Any]) -> MapPoint:
        validated_data["user"] = self.context["request"].user
        return cast(MapPoint, super().create(validated_data))


class MessageSerializer(ModelSerializer):
    point = PrimaryKeyRelatedField(queryset=MapPoint.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ["point", "text"]
        read_only_fields = ["id", "pointcreated_at"]

    def validate_point(self, value: MapPoint) -> MapPoint:
        if not MapPoint.objects.filter(pk=value.pk).exists():
            raise ValidationError("MapPoint does not exist.")
        return value

    def create(self, validated_data: dict[str, Any]) -> Message:
        user = self.context["request"].user
        return Message.objects.create(user=user, **validated_data)
