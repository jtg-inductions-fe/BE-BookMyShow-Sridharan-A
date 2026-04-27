from rest_framework import generics, permissions

from apps.base.models import City, Genre, Language
from apps.base.serializers import CitySerializer, GenreSerializer, LanguageSerializer


class BaseListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]


class LanguageListView(BaseListView):
    """
    GET /api/filters/languages/

    Description:
        - Returns list of all languages
        - Cursor paginated

    Response:
        200 OK
        {
            "next": null,
            "previous": null,
            "results": [
                {
                    "name": string
                }
            ]
        }
    """

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    pagination_class = None


class GenreListView(BaseListView):
    """
    GET /api/filters/genres/

    Description:
        - Returns list of all genres
        - Cursor paginated

    Response:
        200 OK
        {
            "next": null,
            "previous": null,
            "results": [
                {
                    "name": string
                }
            ]
        }
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None


class CityListView(BaseListView):
    """
    GET /api/filters/cities/

    Description:
        - Returns list of all cities
        - Cursor paginated

    Response:
        200 OK
        {
            "next": null,
            "previous": null,
            "results": [
                {
                    "name": string
                }
            ]
        }
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
