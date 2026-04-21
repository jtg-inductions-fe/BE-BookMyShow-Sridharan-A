import contextlib

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, response, status
from rest_framework.views import APIView
from rest_framework_simplejwt import exceptions, tokens, views
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserProfileSerializer, UserRegisterSerializer


def is_mobile_client(req):
    """
    Determines whether request comes from mobile/native client

    Mobile clients must send:
        X-Client-Type: mobile
    """
    return req.headers.get("X-Client-Type") == "mobile"


def set_refresh_cookie(req, res, refresh_token):
    """
    Sets refresh token cookie with `max_age` derived from `SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']`
    Mobile clients receive refresh in response body
    """

    if is_mobile_client(req):
        return

    max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    is_prod = not settings.DEBUG

    res.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        secure=is_prod,
        samesite="None" if is_prod else "Lax",
        path="/api/auth",
        max_age=max_age,
    )


def blacklist_refresh_token(req, res):
    """
    - Blacklists current refresh token
    - Clears refresh token from cookie for web
    """

    refresh = (
        req.data.get("refresh") if is_mobile_client(req) else req.COOKIES.get("refresh")
    )

    if refresh:
        with contextlib.suppress(Exception):
            tokens.RefreshToken(refresh).blacklist()

    if not is_mobile_client(req):
        is_prod = not settings.DEBUG
        res.delete_cookie(
            key="refresh",
            samesite="None" if is_prod else "Lax",
            path="/api/auth",
        )


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.

    Endpoints:
        - POST /api/auth/register/

    Permissons:
        - Alllowany

    Response:
        201 Created
        {
            "detail": User registered successfully,
            "access": string
        }

    Errors:
        400 Bad Request:
            - Validation errors
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Register a new user using email, password and firstname",
        request=UserRegisterSerializer,
        responses={
            201: {"type": "object", "properties": {"message": {"type": "string"}}},
            400: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
        tags=["auth"],
    )
    def post(self, request):
        """
        - Register a new user
        """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        res = response.Response(
            {
                "message": "User registered successfully",
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
        set_refresh_cookie(request, res, str(refresh))

        if is_mobile_client(request):
            res.data["refresh"] = str(refresh)

        return res


class LoginAPIView(APIView):
    """
    API endpoint user login

    Endpoints:
        - POST /api/auth/login/

    Permissions:
        - AllowAny

    Response:
        200 OK
        {
            "detail": User logged in successfully,
            "access": string
        }

    Errors:
        401 Unauthorized:
            - Authentication credentials were not provided
            - Invalid or expired token
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="User login",
        description="Login user using email and password",
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {"type": "string"},
                    "refresh": {"type": "string"},
                },
            },
            400: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
        tags=["auth"],
    )
    def post(self, request):
        """
        - Authenticate user
        - Returns access and refresh token for user if the credentials are valid
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        res = response.Response(
            {
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

        set_refresh_cookie(request, res, str(refresh))

        if is_mobile_client(request):
            res.data["refresh"] = str(refresh)

        return res


class UserProfileAPIView(APIView):
    """
    API Endpoints for accessing and updating current user

    Permissions:
        - IsAuthenticated

    Allowed Endpoints:
        GET /api/auth/user/
        PATCH /api/auth/user/

    GET:
        - Returns current user details

        Response:
            200 OK
            {
                "email": string,
                "first_name": string,
                "last_name": string,
                "phone_number": string
            }

    PATCH:
        - Updates user profile fields

        Request Body:
            {
                "first_name": string,
                "last_name": string,
                "phone_number": string
            }

        Response:
            200 OK
            {
                "email": string
                "first_name": string,
                "last_name": string,
                "phone_number": string
            }

    Errors:
        401 Unauthorized:
            - Authentication credentials were not provided
            - Invalid or expired token
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="User Profile",
        description="Fetch a user details",
        request=UserProfileSerializer,
        responses={
            200: {"type": "object", "properties": {"user": {"type": "object"}}},
            401: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
        tags=["auth"],
    )
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update user details",
        description="Update user details like first_name, last_name, phone_number...",
        request=UserProfileSerializer,
        responses={
            200: {"type": "object", "properties": {"user": {"type": "object"}}},
            401: {"type": "object", "properties": {"message": {"type": "string"}}},
        },
        tags=["auth"],
    )
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/

    Description:
        - Blacklists current refresh token
        - Clears refresh cookie

    Permissions:
        - IsAuthenticated

    Response:
        200 OK
        {
            "message": User logged out successsfully
        }

    Errors:
        401 Unauthorized:
            - Authentication credentials were not provided
            - Invalid or expired token
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, req):
        """
        - Blacklists the previously issued refresh token
        - Clears refresh token from HttpOnly cookie
        """

        res = response.Response(
            {"message": "User logged out successfully"}, status=status.HTTP_200_OK
        )

        blacklist_refresh_token(req, res)

        return res


class TokenRefreshView(views.TokenRefreshView):
    """
    API endpoint for token refresh

    Endpoints:
        - POST /api/auth/token/refresh/

    Permissions:
        - AllowAny

    Response:
        200 OK
        {
            "access": string
        }

    Errors:
        400 Bad Request:
            - Missing refresh token in cookie
        401 Unauthorized:
            - Given refresh token is invalid, blacklisted or expired
    """

    def post(self, req, *args, **kwargs):
        """
        - Overrides post mixin for accessing refresh token from HttpOnly cookie
        - Rotates refresh token, also blacklists previously issued refresh token
        """

        refresh = (
            req.data.get("refresh")
            if is_mobile_client(req)
            else req.COOKIES.get("refresh")
        )

        if not refresh:
            return response.Response(
                {"message": "Refresh token is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # For cases when request.data is immutable
        data = req.data.copy()
        data["refresh"] = refresh

        serializer = self.get_serializer(data=data)

        # Issues error in case of blacklisted refresh token
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError:
            return response.Response(
                {"message": "Given refresh token is invalid, blacklisted or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        new_refresh = serializer.validated_data.pop("refresh")

        res = response.Response(serializer.validated_data, status=status.HTTP_200_OK)

        # Set refresh in cookie for web and in body for mobile
        if new_refresh:
            set_refresh_cookie(req, res, new_refresh)

            if is_mobile_client(req):
                res.data["refresh"] = new_refresh

        return res
