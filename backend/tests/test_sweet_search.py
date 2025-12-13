import pytest
from rest_framework.test import APIClient
from apps.sweets.models import Sweet


@pytest.mark.django_db
def test_search_sweets_by_name(jwt_user_token):
    """
    Search sweets by name (partial match).
    """

    Sweet.objects.create(
        name="Chocolate Cake",
        category="Dessert",
        price=250,
        quantity=10,
    )
    Sweet.objects.create(
        name="Vanilla Ice Cream",
        category="Dessert",
        price=150,
        quantity=5,
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.get("/api/sweets/search/?name=chocolate")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Chocolate Cake"


@pytest.mark.django_db
def test_search_sweets_by_price_range(jwt_user_token):
    """
    Search sweets by price range.
    """

    Sweet.objects.create(
        name="Ladoo",
        category="Indian",
        price=50,
        quantity=20,
    )
    Sweet.objects.create(
        name="Kaju Katli",
        category="Indian",
        price=400,
        quantity=10,
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.get("/api/sweets/search/?min_price=100&max_price=500")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Kaju Katli"
