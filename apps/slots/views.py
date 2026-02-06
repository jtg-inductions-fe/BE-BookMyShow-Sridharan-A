from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.bookings.models import Booking, Seat
from apps.bookings.serializers import SeatSerializer


class BookedSeats(ListAPIView):
    """
    API endpoint for returning booked seats in a slot

    Endpoint:
        - GET /api/slots/<int:pk>/

    Permissions:
        - Allowany

    Response:
        200 OK
        {
            seats: [{"row": int, "number": int}]
        }

    Errors:
        404 Not Found
            - Slot not found
    """

    permission_classes = [AllowAny]
    serializer_class = SeatSerializer
    pagination_class = None

    def get_queryset(self):
        slot_id = self.kwargs.get("pk")
        return Seat.objects.filter(
            booking__slot__id=slot_id, booking__status=Booking.Status.BOOKED
        )
