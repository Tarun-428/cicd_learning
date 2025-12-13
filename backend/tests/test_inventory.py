import pytest
from rest_framework.test import APIClient
from apps.sweets.models import Sweet


@pytest.mark.django_db
def test_user_can_purchase_sweet(jwt_user_token):
    """
    Test that an authenticated user can purchase a sweet
    and quantity decreases by 1.
    """

    sweet = Sweet.objects.create(
        name="Ladoo",
        category="Indian",
        price=10.0,
        quantity=5
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.post(f"/api/sweets/{sweet.id}/purchase/")

    sweet.refresh_from_db()

    assert response.status_code == 200
    assert sweet.quantity == 4


@pytest.mark.django_db
def test_purchase_fails_when_out_of_stock(jwt_user_token):
    """
    Test that purchasing fails if sweet quantity is zero.
    """

    sweet = Sweet.objects.create(
        name="Barfi",
        category="Indian",
        price=15.0,
        quantity=0
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.post(f"/api/sweets/{sweet.id}/purchase/")

    assert response.status_code == 400


@pytest.mark.django_db
def test_admin_can_restock_sweet(jwt_admin_token):
    """
    Test that admin can restock a sweet.
    """

    sweet = Sweet.objects.create(
        name="Jalebi",
        category="Indian",
        price=12.0,
        quantity=2
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")

    response = client.post(
        f"/api/sweets/{sweet.id}/restock/",
        {"quantity": 5},
        format="json"
    )

    sweet.refresh_from_db()

    assert response.status_code == 200
    assert sweet.quantity == 7


@pytest.mark.django_db
def test_non_admin_cannot_restock(jwt_user_token):
    """
    Test that non-admin users cannot restock sweets.
    """

    sweet = Sweet.objects.create(
        name="Peda",
        category="Indian",
        price=8.0,
        quantity=3
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")

    response = client.post(
        f"/api/sweets/{sweet.id}/restock/",
        {"quantity": 5},
        format="json"
    )

    assert response.status_code == 403
