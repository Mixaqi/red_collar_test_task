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
    """Custom DRF GIS field for validating GeoJSON Points safely.

    This field extends `rest_framework_gis.fields.GeometryField` and adds
    comprehensive validation for GeoJSON input, including type, coordinates,
    latitude/longitude ranges, and SRID. All exceptions raised are subclasses
    of 'GeoPointValidationError'. For mode details see README.md

    Validation rules:
        - Input must be a dict with `"type": "Point"` and `"coordinates"` keys.
        - Coordinates must be a list of two numbers: `[longitude, latitude]`.
        - Longitude must be between -180 and 180, latitude between -90 and 90.
        - SRID must be 4326 (WGS84); other SRIDs will raise `InvalidSRIDError`.
        - Invalid GeoJSON raises specific exceptions such as
          'NotAnObjectError', 'InvalidTypeError', 'MissingCoordinatesError',
          'InvalidCoordinatesError', or 'ParseError'.


    Raises:
        NotAnObjectError: If input is not a dict/GeoJSON object.
        InvalidTypeError: If the "type" value is not "Point".
        MissingCoordinatesError: If "coordinates" key is missing or empty.
        InvalidCoordinatesError: If coordinates are not numeric.
        ParseError: If the GeoJSON cannot be parsed into a valid geometry.
        InvalidSRIDError: If the Point's SRID is not 4326.
        InvalidLatitudeError: If latitude is outside -90..90.
        InvalidLongitudeError: If longitude is outside -180..180.
        GeoPointValidationError: Fallback for any other invalid geometry.

    Returns:
        Point: A validated Django `Point` object with SRID 4326.
    """

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
