from django.urls import path

from .views import BookingCancelView, BookingCreateView

urlpatterns = [
    path("", BookingCreateView.as_view(), name="new_booking"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="cancel_booking"),
]
