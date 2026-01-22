from django.db import models

from apps.base.models import TimeStampModel
from apps.cinemas.models import Cinema
from apps.movies.models import Movie


class Slot(TimeStampModel):
    """
    Slot model representing a movie show timing in a cinema.

    Attributes:
        date (date): Date on which the movie is shown.
        start_time (time): Show start time.
        end_time (time): Show end time.
        price (int): Ticket price for the slot.
        movie (ForeignKey): Movie being shown.
        cinema (ForeignKey): Cinema where the movie is shown.
    """

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="slots")
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="slots")

    def __str__(self):
        return f"{self.movie.name} - {self.date} ({self.start_time})"
