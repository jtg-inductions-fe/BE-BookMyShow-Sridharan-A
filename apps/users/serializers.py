from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user model

    Fields:
        "email": string,
        "first_name": string,
        "last_name": string,
        "phone_number": string,
        "password": string
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The email already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login

    Fields:
        "email": string,
        "password": string
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile

    Fields:
        "email": string,
        "first_name": string,
        "last_name": string,
        "phone_number": string,
        "password": string
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
        read_only_fields = ["email"]
