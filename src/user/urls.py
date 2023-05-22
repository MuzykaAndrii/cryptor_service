from django.urls import path

from .views import register_user
from .views import login_user
from .views import logout_user


urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
]
