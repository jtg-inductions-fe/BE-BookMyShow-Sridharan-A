from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


class BookingCreateView(APIView):
    """
    API Endpoint for new booking

    Endpoint:
        - POST /api/bookings/

    Permissions:
        - IsAuthenticated

    Response:
        201 Created
        {
            "results": [
                {
                    "id": int,
                    "slot_id": int,
                    "status": string,
                    "created_at": datetime,
                    "seats": [seat],
                    "total_price": decimal
                }
            ]
        }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )


class UserBookingListView(APIView):
    """
    API Endpoint for booking history of user

    Endpoint:
        - GET /api/bookings/history/

    Permissions:
        - IsAuthenticated

    Response:
        200 OK
        {
            "results": [
                {
                    "id": int,
                    "slot_id": int,
                    "status": int,
                    "created_at": datetime,
                    "seats": [seat],
                    "total_price": decimal
                }
            ]
        }

    Errors:
        401 Unauthorized:
            - Authentication credentials were not provided
            - Invalid or expired token
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = (
            Booking.objects.filter(user=request.user)
            .select_related("slot")
            .prefetch_related("seats")
            .order_by("-created_at")
        )

        return Response(
            BookingSerializer(bookings, many=True).data, status=status.HTTP_200_OK
        )


class BookingCancelView(APIView):
    """
    API Endpoint for cancelling a booking

    Endpoint:
        - PATCH /api/bookings/<int:pk>/cancel/

    Permissions:
        - IsAuthenticated

    Response:
        200 Ok
        {
            "id": int,
            "status" string
        }

    Errors:
        400 Bad Request:
            - Bookings can only be cancelled at least 4 hours before showtime

        401 Unauthorized:
            - Authentication credentials were not provided
            - Invalid or expired token

        404 Not found:
            - Booking not found


    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(
                id=pk,
                user=request.user,
                status=Booking.Status.BOOKED,
            )
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found or cannot be cancelled"},
                status=status.HTTP_404_NOT_FOUND,
            )

        now = timezone.now()
        slot_time = booking.slot.date_time

        if slot_time - now < timedelta(hours=4):
            return Response(
                {
                    "detail": "Bookings can only be cancelled at least 4 hours before showtime"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CANCELLED
        booking.save()

        return Response(
            {"id": booking.id, "status": "CANCELLED"},
            status=status.HTTP_200_OK,
        )
