from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import LoginAPIView, RegisterAPIView, UserProfileAPIView

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="user_register"),
    path("auth/login/", LoginAPIView.as_view(), name="user_login"),
    path(
        "auth/login/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/logout/", jwt_views.TokenBlacklistView.as_view(), name="token_blacklist"
    ),
    path("user/", UserProfileAPIView.as_view(), name="user_profile"),
]
