from typing import Any

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from geopoints.models import MapPoint, Message
from geopoints.serializers import (
    MapPointSerializer,
    MessageSerializer,
    PointSearchSerializer,
)
from geopoints.utils import get_map_point, parse_point


class PointCreateView(CreateAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer
    permission_classes = [IsAuthenticated]


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data.copy()
        location_data = request.data.get("location")

        if not location_data:
            return Response({"detail": "Missing location"}, status=400)

        try:
            point = parse_point(location_data)
        except ValueError as e:
            return Response({"coordinates": str(e)}, status=400)

        map_point = get_map_point(point)
        if not map_point:
            return Response(
                {"detail": "No MapPoint found for these coordinates"}, status=404
            )

        serializer = self.get_serializer(data={**data, "point": map_point.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = serializer.data
        response_data["location"] = {"type": "Point", "coordinates": [point.x, point.y]}

        return Response(response_data, status=201)


class PointSearchView(ListAPIView):
    serializer_class = MapPointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[MapPoint]:
        serializer = PointSearchSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        center_point = Point(
            data["longitude"],
            data["latitude"],
            srid=4326,
        )

        return MapPoint.objects.filter(
            location__distance_lt=(center_point, D(km=data["radius"]))
        )


class MessageSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        query_serializer = PointSearchSerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=400)

        data = query_serializer.validated_data
        center_point = Point(data["longitude"], data["latitude"], srid=4326)
        radius_km = data["radius"]

        messages = Message.objects.filter(
            point__location__distance_lt=(center_point, D(km=radius_km))
        ).select_related("user", "point")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
