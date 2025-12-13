from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import RegisterUserSerializer


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
    

from apps.accounts.serializers import LoginUserSerializer


class LoginUserView(APIView):
    """
    API endpoint for user login.

    POST:
    - Validates username and password
    - Returns user details if authentication succeeds
    """

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response(
                {
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
