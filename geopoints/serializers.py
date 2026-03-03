from typing import Any, cast

from django.db import IntegrityError, transaction
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (
    FloatField,
    Serializer,
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer

from geopoints.exceptions import PointAlreadyExistsError
from geopoints.fields import SafePointField
from geopoints.models import MapPoint, Message


class MapPointSerializer(GeoFeatureModelSerializer):
    """Serializer for the MapPoint model with GeoJSON support.

    Attributes:
        location: Field for validating and saving geographical points.
    """

    location = SafePointField()

    class Meta:
        model = MapPoint
        geo_field = "location"
        fields = ("location", "created_at")

    def create(self, validated_data: dict[str, Any]) -> MapPoint:
        """Creates a new MapPoint for the authenticated user.

        Uses an atomic transaction to prevent duplicate entries and ensure
        data integrity.

        Args:
            validated_data (dict[str, Any]): Validated data containing location information.

        Returns:
            The created MapPoint instance.

        Raises:
            PointAlreadyExistsError: If a point with these coordinates already exists.
        """
        try:
            with transaction.atomic():
                validated_data["user"] = self.context["request"].user
                return cast(MapPoint, super().create(validated_data))
        except IntegrityError as e:
            raise PointAlreadyExistsError() from e


class MessageSerializer(ModelSerializer):
    """Serializer for messages linked to specific map points.

    Attributes:
        location: Geographical point used to link the message (write-only).
    """

    location = SafePointField(write_only=True)

    class Meta:
        model = Message
        fields = ("text", "location", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data: dict[str, Any]) -> Message:
        """Creates a message and associates it with an existing MapPoint.

        Args:
            validated_data (dict[str, Any]): Dictionary containing message text and location geometry.

        Returns:
            The created Message instance.
        """
        point_geom = validated_data.pop("location")
        map_point = get_object_or_404(MapPoint, location=point_geom)
        user = self.context["request"].user
        message = Message.objects.create(point=map_point, user=user, **validated_data)
        return message

    def to_representation(self, instance: Message) -> Any:
        """Convert a Message instance into its serialized representation (JSON with point, created_at fields).

        Args:
            instance (Message): The Message model instance

        Returns:
            Any: A dictionary containing the serialized message data including a GeoJSON
            representation of the associated point and created_at field
        """
        return_value = super().to_representation(instance)
        if instance.point:
            return_value["location"] = {
                "type": "Point",
                "coordinates": [instance.point.location.x, instance.point.location.y],
            }
        return return_value


class PointSearchSerializer(Serializer):
    """Serializer for validating circular area search parameters.

    Attributes:
        latitude(FloatField): Latitude of the search center.
        longitude(FloatField): Longitude of the search center.
        radius(FloatField): Search radius in meters.
    """

    latitude = FloatField(min_value=-90, max_value=90)
    longitude = FloatField(min_value=-180, max_value=180)
    radius = FloatField(min_value=0)
