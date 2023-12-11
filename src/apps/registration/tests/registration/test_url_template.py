from django.urls import reverse_lazy, resolve

from apps.registration.views import RegistrationView
from utils.tests.base import BaseTestCase


class RegistrationViewIntegrationTest(BaseTestCase):
    url: str = reverse_lazy("registration")
    template_name: str = "registration/register.html"

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, RegistrationView)

    # integration
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
