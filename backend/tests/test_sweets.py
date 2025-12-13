import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_admin_can_add_sweet(jwt_admin_token):
    """
    Test that an admin user can add a new sweet.
    Expected:
    - HTTP 201
    - Sweet is created successfully
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")

    payload = {
        "name": "Gulab Jamun",
        "category": "Dessert",
        "price": "20.00",
        "quantity": 50
    }

    response = client.post("/api/sweets/", payload, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Gulab Jamun"


@pytest.mark.django_db
def test_non_admin_cannot_add_sweet(jwt_user_token):
    """
    Test that a non-admin user cannot add a sweet.
    Expected:
    - HTTP 403 Forbidden
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    payload = {
        "name": "Rasgulla",
        "category": "Dessert",
        "price": "15.00",
        "quantity": 30
    }

    response = client.post("/api/sweets/", payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_authenticated_user_can_view_sweets(jwt_user_token):
    """
    Test that an authenticated user can view the list of sweets.
    Expected:
    - HTTP 200
    """

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.get("/api/sweets/")

    assert response.status_code == 200
