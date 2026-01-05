from typing import Any, cast

from django.contrib.gis.geos import GEOSGeometry, Point
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from geopoints.models import MapPoint


class MapPointSerializer(GeoFeatureModelSerializer):
    location = GeometryField()

    class Meta:
        model = MapPoint
        geo_field = "location"
        fields = ("id", "location", "created_at")

    def validate_location(self, geo_value: GEOSGeometry) -> GEOSGeometry:
        if geo_value.hasz:
            raise serializers.ValidationError(
                "Only 2D coordinates (longtitude and latitude) are allowed"
            )
        if not isinstance(geo_value, Point):
            raise serializers.ValidationError(
                f"Use type Point instead of {geo_value.geom_type}."
            )
        return geo_value

    def create(self, validated_data: dict[str, Any]) -> MapPoint:
        validated_data["user"] = self.context["request"].user
        return cast(MapPoint, super().create(validated_data))
