from django.urls import path
from apps.sweets.views import (
    SweetListCreateView,
    PurchaseSweetView,
    RestockSweetView,
    SweetSearchView,
)

urlpatterns = [
    path("", SweetListCreateView.as_view(), name="sweet-list"),
    path("search/", SweetSearchView.as_view(), name="sweet-search"),
    path("<int:sweet_id>/purchase/", PurchaseSweetView.as_view(), name="sweet-purchase"),
    path("<int:sweet_id>/restock/", RestockSweetView.as_view(), name="sweet-restock"),
]
