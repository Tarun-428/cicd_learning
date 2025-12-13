from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.sweets.models import Sweet
from apps.sweets.serializers import SweetSerializer
from apps.sweets.permissions import IsAdminUserRole


class SweetListCreateView(APIView):
    """
    GET:
    - Returns list of all sweets (authenticated users)

    POST:
    - Allows admin users to add a new sweet
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        sweets = Sweet.objects.all()
        serializer = SweetSerializer(sweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "Admin privileges required."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
