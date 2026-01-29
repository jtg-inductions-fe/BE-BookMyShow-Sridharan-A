from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .filters import MovieFilter
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
