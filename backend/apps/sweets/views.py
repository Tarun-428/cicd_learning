from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class SweetListView(APIView):
    """
    Protected endpoint to list sweets.

    Currently returns empty list.
    Will be extended in next steps.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response([], status=status.HTTP_200_OK)
