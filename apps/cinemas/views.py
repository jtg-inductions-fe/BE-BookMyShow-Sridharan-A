from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.slots.models import Slot

from .models import Cinema
from .pagination import CinemaCursorPagination
from .serializers import CinemaSerializer, CinemaSlotSerializer


class CinemaListView(ListAPIView):
    queryset = Cinema.objects.all().select_related("city")
    serializer_class = CinemaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("city__name",)
    pagination_class = CinemaCursorPagination


class CinemaDetailsView(RetrieveAPIView):
    serializer_class = CinemaSlotSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        active_slots = (
            Slot.objects.filter(date_time__gte=timezone.now())
            .select_related(
                "movie",
                "language",
            )
            .order_by("date_time")
        )

        return Cinema.objects.prefetch_related(
            Prefetch("slots", queryset=active_slots, to_attr="active_slots")
        )
