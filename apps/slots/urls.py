from django.urls import path

from .views import BookedSeats

urlpatterns = [path("<int:pk>", BookedSeats.as_view())]
