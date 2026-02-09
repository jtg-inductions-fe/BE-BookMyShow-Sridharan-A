from rest_framework.serializers import ModelSerializer

from apps.base.serializers import LanguageSerializer
from apps.movies.serializers import MovieSerializer

from .models import Slot


class SlotSerializer(ModelSerializer):
    """
    Serializer for Slot model

    Fields:
        "id": int,
        "date_time": datetime,
        "price": decimal,
        "movie": object,
        "language": string,
    """

    movie = MovieSerializer()
    language = LanguageSerializer()

    class Meta:
        model = Slot
        fields = [
            "id",
            "date_time",
            "price",
            "movie",
            "language",
        ]
