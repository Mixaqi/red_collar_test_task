from typing import Any

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from geopoints.models import MapPoint, Message
from geopoints.serializers import MapPointSerializer, MessageSerializer
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
