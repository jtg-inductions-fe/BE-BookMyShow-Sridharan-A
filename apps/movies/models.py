from django.db import models

from apps.base.models import Genre, Language, TimeStampModel


class Movie(TimeStampModel):
    """
    Movie model representing a film available for booking.

    Attributes:
        name (str): Name of the movie.
        description (str): Short description of the movie (optional).
        duration (timedelta): Length of the movie.
        poster (image): Movie poster image.
        release_date (date): Official release date of the movie.
        language (ManyToMany): Languages in which the movie is available.
        genre (ManyToMany): Genres the movie belongs to.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    duration = models.DurationField()
    poster = models.ImageField(upload_to="movie_posters/")
    release_date = models.DateField()
    language = models.ManyToManyField(Language, related_name="movies")
    genre = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return self.name
