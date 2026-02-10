from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.base.models import City, Genre, Language
from apps.bookings.models import Booking, Seat
from apps.cinemas.models import Cinema
from apps.movies.models import Movie
from apps.slots.models import Slot

User = get_user_model()


class TestBookingModel(APITestCase):
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
            name="Test movie",
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

        cls.user = User.objects.create_user(
            email="user1@gmail.com",
            password="user@123",
            first_name="user1",
            last_name="A",
            phone_number="9876543210",
        )

        cls.booking = Booking.objects.create(
            slot=cls.slot, user=cls.user, status=Booking.Status.BOOKED
        )

        cls.seat = Seat.objects.create(row=1, number=1, booking=cls.booking)

    def authenticate(self):
        res = self.client.post(
            "/api/auth/login/", {"email": self.user.email, "password": "user@123"}
        )
        access = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_booking_creation(self):
        self.authenticate()

        res = self.client.post(
            "/api/bookings/",
            {
                "slot_id": self.slot.id,
                "seats": [{"row": 4, "number": 3}, {"row": 4, "number": 4}],
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.test_booking_list()

    def test_booking_list(self):
        self.authenticate()

        res = self.client.get("/api/bookings/history/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cancel_booking(self):
        self.authenticate()

        res = self.client.patch(f"/api/bookings/{self.booking.id}/cancel/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
