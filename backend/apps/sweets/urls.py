from django.urls import path
from apps.sweets.views import SweetListCreateView

urlpatterns = [
    path("", SweetListCreateView.as_view(), name="sweet-list-create"),
    
]
