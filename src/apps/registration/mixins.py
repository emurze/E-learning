from django.contrib import messages
from django.forms import Form
from django.http import HttpResponse
from django.views.generic import FormView

from utils import mixin_for


class SuccessMessageMixin(mixin_for(FormView)):
    """
    Success message mixin for Views that inherited FormMixin or ModelFormMixin
    """

    success_message: str = ""

    def form_valid(self, form: Form) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
