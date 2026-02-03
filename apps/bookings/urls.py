from django.urls import path

from .views import BookingCancelView, BookingCreateView, UserBookingListView

urlpatterns = [
    path("", BookingCreateView.as_view(), name="booking-create"),
    path("list/", UserBookingListView.as_view(), name="user-bookings"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),
]
