from django.forms import Form
from django.views.generic import FormView


class RegistrationView(FormView):
    template_name: str = 'registration/register.html'
    form_class = Form
