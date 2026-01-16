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


class PointCreateView(CreateAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer
    permission_classes = [IsAuthenticated]


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


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
