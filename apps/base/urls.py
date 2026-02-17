from django.urls import path

from apps.base.views import CityListView, GenreListView, LanguageListView

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("cities/", CityListView.as_view(), name="cities"),
    path("languages/", LanguageListView.as_view(), name="languages"),
]
