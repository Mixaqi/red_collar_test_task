from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException


class GeoPointValidationError(ValidationError):
    """Base validation error for GeoJSON Point validation.

    Provides default message and error code that can be overridden
    in subclasses or during initialization.

    Args:
        message (str | None): Optional custom error message.
        code (str | None): Optional custom error code.
    """

    message = "Invalid GeoJSON Point"
    code = "invalid_point"

    def __init__(self, *, message: str | None = None, code: str | None = None) -> None:
        """Initialize the validation error with optional overrides."""
        super().__init__(
            message=message or self.message,
            code=code or self.code,
        )


class NotAnObjectError(GeoPointValidationError):
    """Raised when the provided value is not a GeoJSON object."""

    message = "Value must be a GeoJSON object"
    code = "not_an_object"


class InvalidTypeError(GeoPointValidationError):
    "Raised when the GeoJSON object type is not 'Point'."

    message = "Must be type Point"
    code = "invalid_type"


class MissingCoordinatesError(GeoPointValidationError):
    """Raised when a Point does not contain exactly two coordinates."""

    message = "Point must have two coordinates"
    code = "invalid_format"


class InvalidCoordinatesError(GeoPointValidationError):
    """Raised when coordinates are not numeric values."""

    message = "Coordinates must be numbers"
    code = "invalid_coordinates"


class ParseError(GeoPointValidationError):
    """Raised when a GeoJSON Point cannot be parsed successfully.

    This is typically used in custom DRF fields or serializers when the
    input value cannot be converted into a valid geometry object.

    Example usage(geopoints.fields file):

        try:
            geom = super().to_internal_value(value)
        except ValidationError as e:
            raise ParseError() from e
    """

    message = "Parse error"
    code = "parse_error"


class InvalidSRIDError(GeoPointValidationError):
    """Raised when the Point does not use SRID 4326 (WGS 84). Do not use EPSG 3857"""

    message = "Point must use SRID 4326 (WGS84)"
    code = "invalid_srid"


class InvalidLatitudeError(GeoPointValidationError):
    "Raised when latitude is outside the valid range (-90 to 90)."

    message = "Latitude must be between -90 and 90"
    code = "invalid_latitude"


class InvalidLongitudeError(GeoPointValidationError):
    "Raised when longitude is outside the valid range (-180 to 180)."

    message = "Longitude must be between -180 and 180"
    code = "invalid_longitude"


class PointAlreadyExistsError(APIException):
    """API Exception raised when attempting to create a duplicate point.

    Returns HTTP 409 Conflict
    """

    status_code = 409
    default_detail = "Point already exists"
    default_code = "point_already_exists"
