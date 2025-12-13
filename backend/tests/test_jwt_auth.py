import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_protected_endpoint_requires_authentication():
    """
    Test that accessing a protected endpoint without JWT fails.
    Expected behavior:
    - API returns HTTP 401
    """

    client = APIClient()
    response = client.get("/api/sweets/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_protected_endpoint_allows_authenticated_user():
    """
    Test that authenticated user can access protected endpoint.
    Expected behavior:
    - API returns HTTP 200
    """

    client = APIClient()

    # Register
    client.post(
        "/api/auth/register/",
        {
            "username": "jwtuser",
            "email": "jwt@example.com",
            "password": "StrongPassword123",
        },
        format="json",
    )

    # Login
    login_response = client.post(
        "/api/auth/login/",
        {
            "username": "jwtuser",
            "password": "StrongPassword123",
        },
        format="json",
    )

    token = login_response.data["access_token"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get("/api/sweets/")
    assert response.status_code == 200
