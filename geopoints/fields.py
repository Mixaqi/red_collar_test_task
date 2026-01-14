from typing import Any

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField


class SafePointField(GeometryField):
    def to_internal_value(self, value: Any) -> Point:
        if not isinstance(value, dict):
            raise ValidationError(
                "Invalid GeoJSON Point: must be an object",
                code="not_an_object",
            )

        if value.get("type") != "Point":
            raise ValidationError("Must be type Point", code="invalid_type")

        try:
            geom = super().to_internal_value(value)
        except ValidationError as e:
            raise ValidationError("Parse error", code="parse_error") from e

        if not isinstance(geom, Point):
            raise ValidationError(
                "Only GeoJSON Point is allowed", code="invalid_geojson_point"
            )

        if geom.hasz:
            raise ValidationError(
                "Only 2D coordinates are allowed", code="invalid_geojson_point"
            )

        if geom.srid != 4326:
            raise ValidationError(
                "Point must use SRID 4326 (WGS84)", code="invalid_format"
            )

        lon, lat = geom.coords
        if not (-90 <= lat <= 90):
            raise ValidationError(
                "Latitude must be between -90 and 90", code="invalid_latitude"
            )
        if not (-180 <= lon <= 180):
            raise ValidationError(
                "Longitude must be between -180 and 180", code="invalid_longitude"
            )
        return geom
