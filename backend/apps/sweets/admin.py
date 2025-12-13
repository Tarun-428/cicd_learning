from django.contrib import admin
from apps.sweets.models import Sweet


@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity")
