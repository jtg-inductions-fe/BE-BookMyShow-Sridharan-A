from django_filters import rest_framework as filters

from .models import Cinema


class CinemaFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="city__name", lookup_expr="iexact")

    class Meta:
        model = Cinema
        fields = ["city"]
