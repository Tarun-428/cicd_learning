from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from apps.sweets.models import Sweet
from apps.accounts.permissions import IsAdminUser
from apps.accounts.authentication import JWTAuthentication


class SweetListCreateView(APIView):
    """
    GET:
    - Returns list of all sweets (authenticated users)

    POST:
    - Allows admin users to add a new sweet
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sweets = Sweet.objects.all()
        data = [
            {
                "id": sweet.id,
                "name": sweet.name,
                "category": sweet.category,
                "price": sweet.price,
                "quantity": sweet.quantity,
            }
            for sweet in sweets
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN,
            )

        sweet = Sweet.objects.create(
            name=request.data["name"],
            category=request.data["category"],
            price=request.data["price"],
            quantity=request.data["quantity"],
        )

        return Response(
            {"id": sweet.id, "name": sweet.name},
            status=status.HTTP_201_CREATED,
        )

class PurchaseSweetView(APIView):
    """
    API endpoint to purchase a sweet.

    - Requires authentication
    - Decreases quantity by 1
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, sweet_id):
        sweet = get_object_or_404(Sweet, id=sweet_id)

        if sweet.quantity <= 0:
            return Response(
                {"detail": "Sweet is out of stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        sweet.quantity -= 1
        sweet.save()

        return Response(
            {"message": "Sweet purchased successfully"},
            status=status.HTTP_200_OK
        )

class RestockSweetView(APIView):
    """
    API endpoint to restock a sweet.

    - Admin only
    - Increases quantity
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, sweet_id):
        sweet = get_object_or_404(Sweet, id=sweet_id)
        quantity = request.data.get("quantity")

        if not quantity or int(quantity) <= 0:
            return Response(
                {"detail": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        sweet.quantity += int(quantity)
        sweet.save()

        return Response(
            {"message": "Sweet restocked successfully"},
            status=status.HTTP_200_OK
        )
class SweetSearchView(APIView):
    """
    API endpoint to search sweets.

    Supports filtering by:
    - name (partial match)
    - category
    - min_price
    - max_price
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sweets = Sweet.objects.all()

        name = request.query_params.get("name")
        category = request.query_params.get("category")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if name:
            sweets = sweets.filter(name__icontains=name)

        if category:
            sweets = sweets.filter(category__icontains=category)

        if min_price:
            sweets = sweets.filter(price__gte=min_price)

        if max_price:
            sweets = sweets.filter(price__lte=max_price)

        data = [
            {
                "id": sweet.id,
                "name": sweet.name,
                "category": sweet.category,
                "price": sweet.price,
                "quantity": sweet.quantity,
            }
            for sweet in sweets
        ]

        return Response(data, status=status.HTTP_200_OK)
