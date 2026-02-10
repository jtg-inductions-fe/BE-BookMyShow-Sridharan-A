from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.base.models import City, Genre, Language
from apps.cinemas.models import Cinema
from apps.movies.models import Movie
from apps.slots.models import Slot


class TestCinemaModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.city = City.objects.create(name="Test city")
        cls.genre = Genre.objects.create(name="Action")
        cls.language = Language.objects.create(name="English")

        cls.cinema = Cinema.objects.create(
            name="Test Cinema",
            location="location",
            rows=10,
            seats_per_row=10,
            city=cls.city,
        )

        cls.movie = Movie.objects.create(
            name="Movie Active",
            description="Sample Movie for testing",
            duration=timedelta(hours=3),
            release_date=timezone.localdate(),
        )
        cls.movie.genre.add(cls.genre)
        cls.movie.language.add(cls.language)

        cls.slot = Slot.objects.create(
            date_time=timezone.localtime() + timedelta(days=1),
            price=200,
            movie=cls.movie,
            cinema=cls.cinema,
            language=cls.language,
        )

    def test_cinema_list_success(self):
        res = self.client.get("/api/cinemas/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cinema_list_filters(self):
        res = self.client.get("/api/cinemas/?city__name=Test city")
        cinema_names = [cinema["name"] for cinema in res.data["results"]]

        self.assertIn("Test Cinema", cinema_names)
        self.assertNotIn("Random Cinema", cinema_names)

    def test_cinema_details_and_active_slots(self):
        slug = self.cinema.slug
        res = self.client.get(f"/api/cinemas/{slug}/slots/")
        slot = res.data["movies"][0]["slots"][0]

        self.assertGreaterEqual(slot["date_time"], timezone.localtime())
