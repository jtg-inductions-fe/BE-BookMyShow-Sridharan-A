from rest_framework import permissions, response, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserProfileSerializer, UserRegisterSerializer


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

    def post(self, request):
        """
        - Register a new user
        """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
        )


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

    def post(self, request):
        """
        - Authenticate user
        - Returns access and refresh token for user if the credentials are valid
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return response.Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


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

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return response.Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
