from django.urls import path

from apps.bookings.views import UserBookingListView

from .views import (
    LoginAPIView,
    LogoutView,
    RegisterAPIView,
    TokenRefreshView,
    UserProfileAPIView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="user_register"),
    path("auth/login/", LoginAPIView.as_view(), name="user_login"),
    path(
        "auth/login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("auth/logout/", LogoutView.as_view(), name="token_blacklist"),
    path("user/", UserProfileAPIView.as_view(), name="user_profile"),
    path("user/history/", UserBookingListView.as_view(), name="user_bookings"),
]
