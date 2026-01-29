from rest_framework import serializers

from apps.base.serializers import GenreSerializer, LanguageSerializer

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "description",
            "duration",
            "poster",
            "release_date",
            "language",
            "genre",
            "slug",
        ]
