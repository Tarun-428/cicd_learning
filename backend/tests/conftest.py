import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Returns a DRF API client instance.
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    Creates and returns a normal authenticated user.
    """
    return User.objects.create_user(
        username="normaluser",
        email="user@example.com",
        password="UserPassword123"
    )


@pytest.fixture
def admin_user(db):
    """
    Creates and returns an admin (staff) user.
    """
    return User.objects.create_user(
        username="adminuser",
        email="admin@example.com",
        password="AdminPassword123",
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def jwt_user_token(api_client, user):
    """
    Logs in a normal user and returns a JWT access token.
    """
    response = api_client.post(
        "/api/auth/login/",
        {
            "username": "normaluser",
            "password": "UserPassword123"
        },
        format="json"
    )
    return response.data["access_token"]


@pytest.fixture
def jwt_admin_token(api_client, admin_user):
    """
    Logs in an admin user and returns a JWT access token.
    """
    response = api_client.post(
        "/api/auth/login/",
        {
            "username": "adminuser",
            "password": "AdminPassword123"
        },
        format="json"
    )
    return response.data["access_token"]
