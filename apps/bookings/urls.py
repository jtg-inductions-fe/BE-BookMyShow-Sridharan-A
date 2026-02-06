from django.urls import path

from .views import BookingCancelView, BookingCreateView, UserBookingListView

urlpatterns = [
    path("", BookingCreateView.as_view(), name="new_booking"),
    path("history/", UserBookingListView.as_view(), name="user_bookings"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="cancel_booking"),
]
