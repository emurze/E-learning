from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView

from apps.registration.forms import RegistrationForm

User = get_user_model()


class RegistrationView(FormView):
    template_name: str = 'registration/register.html'
    form_class = RegistrationForm

    def form_valid(self, form: RegistrationForm) -> HttpResponse:
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd['username'],
            password=cd['password'],
        )
        print('form_valid')
        return redirect('/')

    def form_invalid(self, form):
        print(f'form_invalid {form.errors}')
        return super().form_invalid(form)
