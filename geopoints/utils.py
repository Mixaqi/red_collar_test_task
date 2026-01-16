from typing import Any

from django.contrib.gis.geos import Point

from geopoints.models import MapPoint


def parse_point(location_data: dict[str, Any]) -> Point:
    coords = location_data.get("coordinates")

    if not isinstance(coords, (list, tuple)):
        raise ValueError("Coordinates must be a list or tuple")
    if len(coords) != 2:
        raise ValueError(
            "Coordinates must have exactly two elements: [longitude, latitude]"
        )

    try:
        coords = location_data["coordinates"]
        return Point(float(coords[0]), float(coords[1]), srid=4326)
    except (KeyError, TypeError, ValueError):
        raise ValueError("Error occured") from None


def get_map_point(point: Point) -> MapPoint | None:
    try:
        return MapPoint.objects.get(location=point)
    except MapPoint.DoesNotExist:
        return None
