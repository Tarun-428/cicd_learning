import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_can_register_successfully():
    """
    Test that a new user can register with valid data.
    Expected behavior:
    - API returns HTTP 201
    - User is created in the database
    """

    client = APIClient()

    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPassword123"
    }

    response = client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 201
    assert response.data["username"] == "testuser"
    assert response.data["email"] == "testuser@example.com"

@pytest.mark.django_db
def test_registration_fails_for_duplicate_username():
    """
    Test that registration fails if the username already exists.
    Expected behavior:
    - API returns HTTP 400
    """

    client = APIClient()

    payload = {
        "username": "duplicateuser",
        "email": "user1@example.com",
        "password": "StrongPassword123"
    }

    # First registration should succeed
    client.post("/api/auth/register/", payload, format="json")

    # Second registration with same username should fail
    response = client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_fails_for_short_password():
    """
    Test that registration fails when password is too short.
    Expected behavior:
    - API returns HTTP 400
    """

    client = APIClient()

    payload = {
        "username": "shortpassuser",
        "email": "short@example.com",
        "password": "123"
    }

    response = client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_fails_when_required_fields_missing():
    """
    Test that registration fails when required fields are missing.
    Expected behavior:
    - API returns HTTP 400
    """

    client = APIClient()

    payload = {
        "username": "missingfields"
    }

    response = client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 400

@pytest.mark.django_db
def test_user_can_login_with_valid_credentials():
    """
    Test that a registered user can log in with valid credentials.
    Expected behavior:
    - API returns HTTP 200
    - Response contains username
    """

    client = APIClient()

    # Register user first
    register_payload = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "StrongPassword123"
    }
    client.post("/api/auth/register/", register_payload, format="json")

    # Login
    login_payload = {
        "username": "loginuser",
        "password": "StrongPassword123"
    }

    response = client.post("/api/auth/login/", login_payload, format="json")

    assert response.status_code == 200
    assert response.data["username"] == "loginuser"


@pytest.mark.django_db
def test_login_fails_with_invalid_credentials():
    """
    Test that login fails with incorrect password.
    Expected behavior:
    - API returns HTTP 401
    """

    client = APIClient()

    payload = {
        "username": "invaliduser",
        "password": "WrongPassword"
    }

    response = client.post("/api/auth/login/", payload, format="json")

    assert response.status_code == 401
