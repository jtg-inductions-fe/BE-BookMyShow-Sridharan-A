# from .views import CinemaViewSet

from django.urls import path

from .views import CinemaDetailsView, CinemaListView

# router = routers.SimpleRouter()
# router.register(r"", CinemaViewSet)

urlpatterns = [
    path("", CinemaListView.as_view(), name="cinema_list"),
    path("<slug:slug>/slots", CinemaDetailsView.as_view(), name="cinema_detail"),
]
