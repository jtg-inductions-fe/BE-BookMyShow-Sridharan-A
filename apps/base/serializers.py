from rest_framework import serializers

from .models import City, Genre, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["name"]
