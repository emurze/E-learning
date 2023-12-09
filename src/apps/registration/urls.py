from django.urls import path

from .views import RegistrationView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
]
