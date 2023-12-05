from django.urls import resolve, reverse_lazy

from .base import BaseTestCase
from apps.registration.views import RegistrationView


class RegistrationViewIntegrationTest(BaseTestCase):
    url: str = reverse_lazy('registration')
    template_name: str = 'registration/register.html'

    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, RegistrationView)

    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
