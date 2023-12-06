from unittest import skip

from django.urls import reverse_lazy
from django.test import Client

from apps.registration.forms import RegistrationForm
from apps.registration.tests.base import BaseTestCase
from apps.registration.views import RegistrationView


class RegistrationViewTestCase(BaseTestCase):
    url: str = reverse_lazy('registration')
    view_class = RegistrationView
    redirect_url: str = '/'

    def test_content_registration_form(self) -> None:
        request = self.request_factory.get(self.url)
        response = self.view_class.as_view()(request)

        self.assertIsInstance(
            response.context_data.get('form'),
            RegistrationForm,
        )

    @skip
    def test_form_valid_redirect(self) -> None:
        request = self.request_factory.post(self.url, data={
            'username': 'vlad',
            'password': 12345678,
            'password2': 12345678,
        })
        response = self.view_class.as_view()(request)
        response.client = Client()

        self.assertRedirects(response, self.redirect_url)
