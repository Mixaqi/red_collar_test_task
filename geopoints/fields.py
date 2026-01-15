from typing import Any

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField


class SafePointField(GeometryField):
    def to_internal_value(self, value: Any) -> Point:
        match value:
            case {"type": "Point", "coordinates": [lon, lat]} if type(lon) in (
                int,
                float,
            ) and type(lat) in (int, float):
                pass

            case {"type": "Point", "coordinates": [_, _]}:
                raise ValidationError(
                    "Coordinates must be numbers", code="invalid_coordinates"
                )

            case {"type": "Point"}:
                raise ValidationError(
                    "Point must have two coordinates", code="invalid_format"
                )

            case {"type": str(_)}:
                raise ValidationError("Must be type Point", code="invalid_type")

            case _:
                raise ValidationError(
                    "Invalid GeoJSON Point: must be an object with 'type' and 'coordinates'",
                    code="not_an_object",
                )

        try:
            geom = super().to_internal_value(value)
        except ValidationError as e:
            raise ValidationError("Parse error", code="parse_error") from e

        match geom:
            case Point(hasz=True):
                raise ValidationError(
                    "Only 2D coordinates are allowed", code="invalid_geojson_point"
                )
            case Point(srid=srid) if srid != 4326:
                raise ValidationError(
                    "Point must use SRID 4326 (WGS84)", code="invalid_structure"
                )
            case Point(coords=(lon, lat)):
                if not (-90 <= lat <= 90):
                    raise ValidationError(
                        "Latitude must be between -90 and 90", code="invalid_latitude"
                    )
                if not (-180 <= lon <= 180):
                    raise ValidationError(
                        "Longitude must be between -180 and 180",
                        code="invalid_longitude",
                    )
            case _:
                raise ValidationError(
                    "Only GeoJSON Point is allowed", code="invalid_geojson_point"
                )

        return geom
