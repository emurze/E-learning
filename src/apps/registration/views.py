from django.contrib.auth import get_user_model
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.registration.forms import RegistrationForm
from apps.registration.mixins import SuccessMessageMixin

User = get_user_model()
REGISTRATION_SUCCESS_MESSAGE = "Registration has been successful"


class RegistrationView(
    SuccessMessageMixin,
    FormView,
):
    template_name: str = "registration/register.html"
    form_class: Form = RegistrationForm
    success_url: str = reverse_lazy("login")
    success_message: str = REGISTRATION_SUCCESS_MESSAGE

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd["username"],
            password=cd["password"],
        )
        return super().form_valid(form)
