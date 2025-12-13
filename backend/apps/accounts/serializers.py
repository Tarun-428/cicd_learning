from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Performs:
    - Required field validation
    - Password length validation
    - Unique username validation
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        """
        Ensure the username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        """
        Create and return a new user with a hashed password.
        """
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

from django.contrib.auth import authenticate


class LoginUserSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates:
    - Username
    - Password
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Authenticate user with provided credentials.
        """
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        data["user"] = user
        return data
