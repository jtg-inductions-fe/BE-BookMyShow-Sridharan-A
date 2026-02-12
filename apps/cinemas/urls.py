from django.urls import path

from .views import CinemaDetailsView, CinemaListView

urlpatterns = [
    path("", CinemaListView.as_view(), name="cinema_list"),
    path("<slug:slug>/slots/", CinemaDetailsView.as_view(), name="cinema_detail"),
]
