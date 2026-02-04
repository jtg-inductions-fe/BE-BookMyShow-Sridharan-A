from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import LoginAPIView, RegisterAPIView, UserProfileAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="user_register"),
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", jwt_views.TokenBlacklistView.as_view(), name="token_blacklist"),
    path("user/", UserProfileAPIView.as_view(), name="user_profile"),
]
