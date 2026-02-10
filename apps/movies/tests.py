from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.base.models import City, Genre, Language
from apps.cinemas.models import Cinema
from apps.movies.models import Movie
from apps.slots.models import Slot


class TestMovieModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name="Action")
        cls.language = Language.objects.create(name="English")
        cls.city = City.objects.create(name="Test city")

        cls.movie_active = Movie.objects.create(
            name="Movie Active",
            description="Sample Movie for testing",
            duration=timedelta(hours=3),
            release_date=timezone.localdate(),
        )
        cls.movie_active.genre.add(cls.genre)
        cls.movie_active.language.add(cls.language)

        cls.movie_inactive = Movie.objects.create(
            name="Movie InActive",
            description="Sample Movie for testing",
            duration=timedelta(hours=3),
            release_date=timezone.localdate(),
        )
        cls.movie_inactive.genre.add(cls.genre)
        cls.movie_inactive.language.add(cls.language)

        cls.cinema = Cinema.objects.create(
            name="Test Cinema",
            location="location",
            rows=10,
            seats_per_row=10,
            city=cls.city,
        )

        cls.slot = Slot.objects.create(
            date_time=timezone.localtime() + timedelta(days=1),
            price=200,
            movie=cls.movie_active,
            cinema=cls.cinema,
            language=cls.language,
        )

    def test_movie_list_success(self):
        res = self.client.get("/api/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_movie_list_returns_active_movies(self):
        res = self.client.get("/api/movies/")
        movie_names = [movie["name"] for movie in res.data["results"]]
        self.assertIn("Movie Active", movie_names)
        self.assertNotIn("Movie NotActive", movie_names)

    def test_movie_list_filters(self):
        genre_res = self.client.get("/api/movies/?genre=Action")
        movie_names = [movie["name"] for movie in genre_res.data["results"]]

        self.assertIn("Movie Active", movie_names)
        self.assertNotIn("Different Genre", movie_names)

        language_res = self.client.get("/api/movies/?language=English")
        movie_names = [movie["name"] for movie in language_res.data["results"]]

        self.assertIn("Movie Active", movie_names)
        self.assertNotIn("Different Language", movie_names)

    def test_movie_details_success(self):
        slug = self.movie_active.slug
        res = self.client.get(f"/api/movies/{slug}/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "Movie Active")

    def test_movie_slots_returns_active_slots(self):
        slug = self.movie_active.slug
        res = self.client.get(f"/api/movies/{slug}/slots/")
        slot = res.data["cinemas"][0]["slots"][0]

        self.assertGreaterEqual(slot["date_time"], timezone.localtime())
