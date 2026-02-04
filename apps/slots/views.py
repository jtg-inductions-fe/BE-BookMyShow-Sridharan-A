from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.bookings.models import Booking, Seat
from apps.bookings.serializers import SeatSerializer


class BookedSeats(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SeatSerializer

    def get_queryset(self):
        slot_id = self.kwargs.get("pk")
        return Seat.objects.filter(
            booking__slot__id=slot_id, booking__status=Booking.Status.BOOKED
        )
