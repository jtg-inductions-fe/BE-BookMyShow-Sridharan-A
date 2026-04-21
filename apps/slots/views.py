from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.bookings.models import Booking, Seat
from apps.bookings.serializers import SeatSerializer

from .models import Slot


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

    def list(self, request, *args, **kwargs):
        slot_id = self.kwargs.get("pk")

        queryset = self.get_queryset()
        seats = self.get_serializer(queryset, many=True).data

        # get slot
        slot = Slot.objects.select_related("cinema").get(pk=slot_id)

        return Response(
            {
                "slot_id": slot.id,
                "movie": slot.movie.name,
                "cinema": slot.cinema.name,
                "date_time": slot.date_time,
                "price": slot.price,
                "rows": slot.cinema.rows,
                "seats_per_row": slot.cinema.seats_per_row,
                "booked_seats": seats,
            }
        )
