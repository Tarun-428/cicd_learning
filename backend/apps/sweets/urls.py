from django.urls import path
from apps.sweets.views import SweetListView

urlpatterns = [
    path("", SweetListView.as_view(), name="sweet-list"),
]
