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
    """
    API endpoint for listing cinemas

    Endpoint:
        - GET /api/cinemas/

    Permissons:
        - Allowany

    Description:
    - Returns list of cinemas
    - Supports filtering by city
    - Cursor paginated

    Response:
        200 OK
        {
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": int,
                    "name": string,
                    "location": string,
                    "rows": int,
                    "seats_per_row": int,
                    "city": string,
                    "slug": string
                }
            ]
        }
    """

    queryset = Cinema.objects.all().select_related("city")
    serializer_class = CinemaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("city__name",)
    pagination_class = CinemaCursorPagination


class CinemaDetailsView(RetrieveAPIView):
    """
    API Endpoint for retrieving details of a single cinema with slots

    Endpoint:
        - GET /api/cinemas/<slug>/slots

    Permissions:
        - Allowany

    Response:
        200 OK
        {
            "id": int,
            "name": string,
            "location": string,
            "duration": string,
            "rows": int,
            "seats_per_row": int,
            "movies": [slots]
        }

    Errors:
        404 Not Found:
            - Cinema Not Found
    """

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
