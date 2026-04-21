import django_filters
from django.utils import timezone
from django_filters import rest_framework as filters

from .models import Movie


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    """
    Enables filtering like ?language=English,Tamil
    """


class MovieFilter(filters.FilterSet):
    language = CharInFilter(
        field_name="language__name", lookup_expr="in", distinct=True
    )
    genre = CharInFilter(field_name="genre__name", lookup_expr="in", distinct=True)

    release_date = django_filters.DateFilter(
        field_name="release_date", lookup_expr="gte"
    )

    city = filters.CharFilter(method="filter_by_city")

    def filter_by_city(self, queryset, name, value):
        return queryset.filter(
            slots__date_time__gte=timezone.now(),
            slots__cinema__city__name__iexact=value,
        ).distinct()

    class Meta:
        model = Movie
        fields = ["language", "genre", "release_date", "city"]
