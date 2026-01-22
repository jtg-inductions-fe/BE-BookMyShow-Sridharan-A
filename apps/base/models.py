from django.db import models


class TimeStampModel(models.Model):
    """
    Abstract base model that adds timestamp fields to child models.

    Fields:
        created_at:
            Automatically set when the record is created.

        updated_at:
            Automatically updated every time the record is saved.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Marks this model as abstract (no table will be created)
        abstract = True


class Language(TimeStampModel):
    """
    Language model:

    Fields:
        name:
            name of the language
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(TimeStampModel):
    """
    Genre model:

    Fields:
        name:
            name of the genre
    """

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class City(TimeStampModel):
    """
    City model:

    Fields:
        name:
            name of the city
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
