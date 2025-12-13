from django.contrib import admin
from apps.sweets.models import Sweet


@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    """
    Admin configuration for Sweet model.
    """

    list_display = ("id", "name", "category", "price", "quantity", "created_at")
    search_fields = ("name", "category")
    list_filter = ("category",)
