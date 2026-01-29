from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Cinema
from .serializers import CinemaSerializer, CinemaSlotSerializer


class CinemaListView(ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("city__name",)


class CinemaDetailsView(RetrieveAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSlotSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
