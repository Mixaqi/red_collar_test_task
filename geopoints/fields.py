from typing import Any

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField

from geopoints.exceptions import (
    GeoPointValidationError,
    InvalidCoordinatesError,
    InvalidLatitudeError,
    InvalidLongitudeError,
    InvalidSRIDError,
    InvalidTypeError,
    MissingCoordinatesError,
    NotAnObjectError,
    ParseError,
)


class SafePointField(GeometryField):
    def to_internal_value(self, value: Any) -> Point:
        match value:
            case {"type": "Point", "coordinates": [lon, lat]} if type(lon) in (
                int,
                float,
            ) and type(lat) in (int, float):
                pass

            case {"type": "Point", "coordinates": [_, _]}:
                raise InvalidCoordinatesError()

            case {"type": "Point"}:
                raise MissingCoordinatesError()

            case {"type": str(_)}:
                raise InvalidTypeError()

            case _:
                raise NotAnObjectError()

        try:
            geom = super().to_internal_value(value)
        except ValidationError as e:
            raise ParseError() from e

        match geom:
            case Point(srid=srid) if srid != 4326:
                raise InvalidSRIDError()
            case Point(coords=(lon, lat)):
                if not (-90 <= lat <= 90):
                    raise InvalidLatitudeError()
                if not (-180 <= lon <= 180):
                    raise InvalidLongitudeError()
            case _:
                raise GeoPointValidationError()

        return geom
