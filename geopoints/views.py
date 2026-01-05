from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from geopoints.models import MapPoint
from geopoints.serializers import MapPointSerializer


class PointCreateView(CreateAPIView):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer
    permission_classes = [IsAuthenticated]
