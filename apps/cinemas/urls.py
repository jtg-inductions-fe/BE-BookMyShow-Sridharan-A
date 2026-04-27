from django.urls import path

from .views import CinemaDetailsView, CinemaListView

urlpatterns = [
    path("cinemas", CinemaListView.as_view(), name="cinema_list"),
    path(
        "cinemas/<slug:slug>/slots", CinemaDetailsView.as_view(), name="cinema_detail"
    ),
]
