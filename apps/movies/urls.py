from django.urls import path
from rest_framework import routers

from .views import (
    MovieSlotsPerCinemaListView,
    MovieViewSet,
)

router = routers.SimpleRouter()
router.register(r"", MovieViewSet)
urlpatterns = [
    path(
        "<slug:slug>/slots/",
        MovieSlotsPerCinemaListView.as_view(),
        name="movie_slots_per_cinemas",
    ),
]
urlpatterns += router.urls
