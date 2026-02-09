from rest_framework import serializers

from apps.base.serializers import GenreSerializer, LanguageSerializer

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model

    Fields:
        "id": int,
        "name": string,
        "description": string,
        "duration": time,
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
    """

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


class MovieSlotsPerCinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie Slots

    Fields:
        "id": int,
        "name": string,
        "description": string,
        "duration": time,
        "poster": string,
        "release_date": date,
        "slug": string,
        "cinemas": [cinema[slots]],
    """

    cinemas = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "description",
            "duration",
            "poster",
            "release_date",
            "slug",
            "cinemas",
        ]

    def get_cinemas(self, movie):
        cinema_map = {}
        slots = getattr(movie, "active_slots", [])
        for slot in slots:
            cinema = slot.cinema

            if cinema.id not in cinema_map:
                cinema_map[cinema.id] = {
                    "id": cinema.id,
                    "name": cinema.name,
                    "location": cinema.location,
                    "slug": cinema.slug,
                    "slots": [],
                }

            cinema_map[cinema.id]["slots"].append(
                {
                    "id": slot.id,
                    "date_time": slot.date_time,
                    "price": slot.price,
                    "language": {"name": slot.language.name},
                }
            )

        return list(cinema_map.values())
