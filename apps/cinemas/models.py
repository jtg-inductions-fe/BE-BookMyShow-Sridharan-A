from django.db import models
from django.utils.text import slugify

from apps.base.models import City, TimeStampModel


class Cinema(TimeStampModel):
    """
    Cinema model representing a movie theatre location.

    Attributes:
        name (str): Name of the cinema.
        location (str): Address or area of the cinema.
        rows (int): Number of seating rows in the cinema.
        seats_per_rows (int): Number of seats in each row.
        city (ForeignKey): City in which the cinema is located.
    """

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="cinemas")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}-{self.city.name}")
            slug = base
            i = 1
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location", "city"],
                name="unique_cinema_per_location_city",
            )
        ]

    def __str__(self):
        return self.name
