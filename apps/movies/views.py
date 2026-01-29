from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.slots.models import Slot

from .filters import MovieFilter
from .models import Movie
from .serializers import MovieCinemaSerializer, MovieSerializer


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter


class MovieDetailsView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class MovieCinemaListView(RetrieveAPIView):
    serializer_class = MovieCinemaSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        active_slots = Slot.objects.filter(
            date_time__gte=timezone.now()
        ).select_related(
            "cinema",
            "language",
        )

        return Movie.objects.prefetch_related(
            Prefetch(
                "slots",
                queryset=active_slots,
                to_attr="active_slots",
            )
        )
