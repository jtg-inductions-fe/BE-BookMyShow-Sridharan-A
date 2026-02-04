from django.urls import path

from .views import (
    MovieCinemaListView,
    MovieDetailsView,
    MovieListView,
)

urlpatterns = [
    path("", MovieListView.as_view(), name="movie-list"),
    path("<slug:slug>/", MovieDetailsView.as_view(), name="movie-detail"),
    path("<slug:slug>/slots/", MovieCinemaListView.as_view(), name="movie-cinemas"),
]
