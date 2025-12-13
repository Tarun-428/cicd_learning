from rest_framework import serializers
from apps.sweets.models import Sweet


class SweetSerializer(serializers.ModelSerializer):
    """
    Serializer for Sweet model.
    Handles validation and serialization of sweet data.
    """

    class Meta:
        model = Sweet
        fields = ("id", "name", "category", "price", "quantity")
