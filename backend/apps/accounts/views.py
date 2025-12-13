from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import RegisterUserSerializer
from apps.accounts.serializers import LoginUserSerializer



class RegisterUserView(APIView):
    """
    API endpoint for user registration.

    POST:
    - Accepts username, email, password
    - Creates a new user
    - Returns created user data
    """

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.exceptions import ValidationError


class LoginUserView(APIView):
    """
    API endpoint for user login with JWT.
    """

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
