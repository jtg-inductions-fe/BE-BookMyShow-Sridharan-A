from django.urls import path
from rest_framework import routers

from .views import (
    MovieSlotsPerCinemaListView,
    MovieViewSet,
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"movies", MovieViewSet)
urlpatterns = [
    path(
        "movies/<slug:slug>/slots",
        MovieSlotsPerCinemaListView.as_view(),
        name="movie_slots_per_cinemas",
    ),
]
urlpatterns += router.urls
