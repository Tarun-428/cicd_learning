from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.conf import settings
import jwt


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class.

    - Expects token in Authorization header
    - Returns None if no credentials (DRF will decide)
    - Raises AuthenticationFailed for invalid token
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        # IMPORTANT:
        # Return None when no header is present
        # This allows DRF to issue a 401 challenge
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")

            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix.")

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token.")
        except ValueError:
            raise AuthenticationFailed("Invalid authorization header.")

        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        return (user, None)

    def authenticate_header(self, request):
        """
        This method tells DRF to return 401 instead of 403
        when authentication is required but missing.
        """
        return "Bearer"
