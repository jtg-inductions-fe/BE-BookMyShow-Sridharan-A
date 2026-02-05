from django.urls import path

from .views import (
    MovieDetailsView,
    MovieListView,
    MovieSlotsPerCinemaListView,
)

urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("<slug:slug>/", MovieDetailsView.as_view(), name="movie-detail"),
    path(
        "<slug:slug>/slots/",
        MovieSlotsPerCinemaListView.as_view(),
        name="movie-cinemas",
    ),
]
