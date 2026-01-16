from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException


class GeoPointValidationError(ValidationError):
    message = "Invalid GeoJSON Point"
    code = "invalid_point"

    def __init__(self, *, message: str | None = None, code: str | None = None) -> None:
        super().__init__(
            message=message or self.message,
            code=code or self.code,
        )


class NotAnObjectError(GeoPointValidationError):
    message = "Value must be a GeoJSON object"
    code = "not_an_object"


class InvalidTypeError(GeoPointValidationError):
    message = "Must be type Point"
    code = "invalid_type"


class MissingCoordinatesError(GeoPointValidationError):
    message = "Point must have two coordinates"
    code = "invalid_format"


class InvalidCoordinatesError(GeoPointValidationError):
    message = "Coordinates must be numbers"
    code = "invalid_coordinates"


class ParseError(GeoPointValidationError):
    message = "Parse error"
    code = "parse_error"


class InvalidSRIDError(GeoPointValidationError):
    message = "Point must use SRID 4326 (WGS84)"
    code = "invalid_srid"


class InvalidLatitudeError(GeoPointValidationError):
    message = "Latitude must be between -90 and 90"
    code = "invalid_latitude"


class InvalidLongitudeError(GeoPointValidationError):
    message = "Longitude must be between -180 and 180"
    code = "invalid_longitude"


class PointAlreadyExistsError(APIException):
    status_code = 409
    default_detail = "Point already exists"
    default_code = "point_already_exists"
