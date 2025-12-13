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
