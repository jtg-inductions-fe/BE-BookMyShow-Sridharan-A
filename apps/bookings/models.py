from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.base.models import TimeStampModel
from apps.slots.models import Slot


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
        PENDING = 2

    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")

    def __str__(self):
        return f"Booking #{self.id} - {self.user.email}"


class Seat(TimeStampModel):
    """
    Seat model linking seats to a booking and slot.

    Attributes:
        row (str): Seat row identifier (e.g., A, B, C).
        number (int): Seat number within the row.
        booking (ForeignKey): Booking reference.
    """

    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="seats")

    def clean(self):
        super().clean()

        booking_cinema = self.booking.slot.cinema

        if self.row < 1 or self.row > booking_cinema.rows:
            raise ValidationError(
                f" Row must be greater than 0 and lesser than {booking_cinema.rows}"
            )

        if self.number < 1 or self.number > booking_cinema.seats_per_row:
            raise ValidationError(
                f"Seat number must be greater than 0 and less than {booking_cinema.seats_per_row}"
            )

        already_booked = (
            Seat.objects.filter(
                booking__slot_id=self.booking.slot_id,
                booking__status=Booking.Status.BOOKED,
                row=self.row,
                number=self.number,
            )
            .exclude(pk=self.pk)
            .exists()
        )

        if already_booked:
            raise ValidationError(
                f"The Seat(Row : {self.row} Seat_Number : {self.number}) has been already booked"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.row} - {self.number}"
