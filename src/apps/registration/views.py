from django.contrib.auth import get_user_model
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.registration.forms import RegistrationForm

User = get_user_model()


class RegistrationView(FormView):
    template_name: str = 'registration/register.html'
    form_class: Form = RegistrationForm
    success_url: str = reverse_lazy('home:home')

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd['username'],
            password=cd['password'],
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
