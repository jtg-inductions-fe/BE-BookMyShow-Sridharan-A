from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.base.models import Language, TimeStampModel
from apps.cinemas.models import Cinema
from apps.movies.models import Movie


class Slot(TimeStampModel):
    """
    Slot model representing a movie show timing in a cinema.

    Attributes:
        date_time (datetime): Date and time when the movie is shown.
        price (int): Ticket price for the slot.
        movie (ForeignKey): Movie being shown.
        cinema (ForeignKey): Cinema where the movie is shown.
        language (ForeignKey): Language in which the movie is shown.
    """

    date_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="slots")
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="slots")
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="slots"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date_time", "movie", "cinema"],
                name="unique_slot_per_movie_cinema_date_time",
            )
        ]

    def clean(self):
        super().clean()
        if self.date_time < timezone.now():
            raise ValidationError("Cannot create slot for past dates")

        if self.date_time.date() < self.movie.release_date:
            raise ValidationError(
                "Cannot create slot for a movie before it's release date"
            )

        if not self.movie.language.filter(pk=self.language.pk).exists():
            raise ValidationError(
                "Cannot create slot for a movie with language which is not in movie's languages"
            )

        prev_slot = (
            Slot.objects.filter(cinema=self.cinema, date_time__lt=self.date_time)
            .exclude(pk=self.pk)
            .order_by("-date_time")
            .first()
        )

        if prev_slot:
            prev_end_time = prev_slot.date_time + prev_slot.movie.duration
            if self.date_time < prev_end_time:
                raise ValidationError(
                    f"Slot overlaps with previous movie ending at {prev_end_time}."
                )

        next_slot = (
            Slot.objects.filter(cinema=self.cinema, date_time__gt=self.date_time)
            .exclude(pk=self.pk)
            .order_by("date_time")
            .first()
        )

        if next_slot:
            current_end_time = self.date_time + self.movie.duration
            if current_end_time > next_slot.date_time:
                raise ValidationError(
                    f"Slot overlaps with next movie starting at {next_slot.date_time}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.name} - {self.date_time}"
