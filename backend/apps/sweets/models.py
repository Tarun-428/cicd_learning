from django.db import models


class Sweet(models.Model):
    """
    Represents a sweet item in the shop inventory.
    """

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
