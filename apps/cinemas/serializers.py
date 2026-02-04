from rest_framework import serializers

from apps.base.serializers import CitySerializer

from .models import Cinema


class CinemaSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "location",
            "rows",
            "seats_per_row",
            "city",
            "slug",
        ]


class CinemaSlotSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = [
            "id",
            "name",
            "location",
            "rows",
            "seats_per_row",
            "city",
            "movies",
        ]

    def get_movies(self, cinema):
        movie_map = {}

        slots = getattr(cinema, "active_slots", [])
        for slot in slots:
            movie = slot.movie

            if movie.id not in movie_map:
                movie_map[movie.id] = {
                    "id": movie.id,
                    "name": movie.name,
                    "slug": movie.slug,
                    "slots": [],
                }
            movie_map[movie.id]["slots"].append(
                {
                    "id": slot.id,
                    "date_time": slot.date_time,
                    "price": slot.price,
                    "language": slot.language.name,
                }
            )
        return list(movie_map.values())
