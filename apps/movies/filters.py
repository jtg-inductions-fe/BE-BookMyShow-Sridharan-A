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

    class Meta:
        model = Movie
        fields = ["language", "genre"]
