from datetime import datetime, time

from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.utils import timezone
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.slots.models import Slot

from .filters import MovieFilter
from .models import Movie
from .pagination import MovieCursorPagination
from .serializers import MovieSerializer, MovieSlotsPerCinemaSerializer


class MovieViewSet(ReadOnlyModelViewSet):
    """
    API endpoint for listing movies

    Endpoint:
        - GET /api/movies/

    Permissons:
        - Allowany

    Description:
    - Returns list of movies
    - Supports filtering by genre, language
    - Cursor paginated

    Response:
        200 OK
        {
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 0,
                    "name": string,
                    "description": string,
                    "duration": string",
                    "poster": string",
                    "release_date": date,
                    "language": [
                        {
                        "name": string
                        }
                    ],
                    "genre": [
                        {
                        "name": string
                        }
                    ],
                    "slug": string
                }
            ]
        }
    """

    queryset = (
        Movie.objects.filter(slots__date_time__gte=timezone.now())
        .distinct()
        .prefetch_related("language", "genre")
        .order_by("-release_date")
    )

    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = MovieCursorPagination
    lookup_field = "slug"

    @property
    def filterset_class(self) -> type[filters.FilterSet] | None:
        if self.action == "list":
            return MovieFilter


class MovieSlotsPerCinemaListView(RetrieveAPIView):
    """
    API Endpoint for retrieving slots for a single movie grouped by cinemas

    Endpoint:
        - GET /api/movies/<slug>/slots/

    Permissions:
        - Allowany

    Response:
        200 OK
        {
            "id": int,
            "name": string,
            "description": string,
            "duration": string,
            "poster": string,
            "release_date": date,
            "slug": string,
            "cinemas": [slots]
        }

    """

    serializer_class = MovieSlotsPerCinemaSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        date = self.request.query_params.get("date")
        today = timezone.localdate()

        if date:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            selected_date = timezone.localdate()

        if selected_date < today:
            raise ValidationError("Date cannot be in the past")

        day_start = timezone.make_aware(datetime.combine(selected_date, time.min))

        day_end = timezone.make_aware(datetime.combine(selected_date, time.max))

        if selected_date == timezone.localdate():
            slot_filter = {
                "date_time__gte": timezone.now(),
                "date_time__lte": day_end,
            }
        else:
            slot_filter = {
                "date_time__range": (day_start, day_end),
            }

        active_slots = (
            Slot.objects.filter(**slot_filter)
            .select_related(
                "cinema",
                "language",
            )
            .order_by("date_time")
        )

        return Movie.objects.prefetch_related(
            Prefetch(
                "slots",
                queryset=active_slots,
                to_attr="active_slots",
            )
        )
