from django.db import models

from apps.base.models import TimeStampModel
from apps.slots.models import Slot
from apps.users.models import User


class Booking(TimeStampModel):
    """
    Booking model representing a user's ticket purchase.

    Attributes:
        status (int): Booking status (BOOKED or CANCELLED).
        user (ForeignKey): User who made the booking.
        slot (ForeignKey): Slot for which the booking was made.
    """

    class Status(models.IntegerChoices):
        CANCELLED = 0
        BOOKED = 1

    status = models.IntegerField(choices=Status.choices, default=Status.BOOKED)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email}"


class Seat(TimeStampModel):
    """
    Seat model representing a physical seat in a cinema.

    Attributes:
        row (str): Seat row identifier (e.g., A, B, C).
        number (int): Seat number within the row.
    """

    row = models.CharField(max_length=1)
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.row}{self.number}"


class BookingSeat(TimeStampModel):
    """
    BookingSeat model linking seats to a booking and slot.

    Attributes:
        booking (ForeignKey): Booking reference.
        seat (ForeignKey): Seat being booked.
        slot (ForeignKey): Slot for which the seat is booked.
    """

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booking_seats"
    )
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE, related_name="booking_seats"
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name="booking_seats"
    )

    def __str__(self):
        return f"{self.seat} - {self.slot}"
