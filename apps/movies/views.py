from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.slots.models import Slot

from .filters import MovieFilter
from .models import Movie
from .pagination import MovieCursorPagination
from .serializers import MovieSerializer, MovieSlotsPerCinemaSerializer


class MovieListView(ListAPIView):
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
    filterset_class = MovieFilter
    pagination_class = MovieCursorPagination


class MovieDetailsView(RetrieveAPIView):
    """
    API Endpoint for retrieving details of a single movie

    Endpoint:
        - GET /api/movies/<slug>

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

    Errors:
        404 Not Found:
            - Movie Not Found
    """

    queryset = Movie.objects.all().prefetch_related("language", "genre")
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


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
        active_slots = (
            Slot.objects.filter(date_time__gte=timezone.now())
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
