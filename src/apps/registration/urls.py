from django.urls import path

from .views import RegistrationView, MyLoginView, MyLogoutView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
