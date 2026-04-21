from django.urls import path

from .views import BookedSeats

urlpatterns = [path("slots/<int:pk>", BookedSeats.as_view())]
