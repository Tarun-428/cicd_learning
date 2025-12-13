from django.urls import path
from apps.accounts.views import RegisterUserView, LoginUserView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="user-register"),
    path("login/", LoginUserView.as_view(), name="user-login"),
]
