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
