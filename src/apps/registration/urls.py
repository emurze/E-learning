from django.urls import path

from .views import RegistrationView, MyLoginView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", MyLoginView.as_view(), name="login"),
]
