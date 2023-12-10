from django.contrib.auth.views import LoginView
from django.urls import resolve, reverse_lazy

from apps.registration.views import RegistrationView, MyLoginView
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


class MyLoginViewIntegrationTest(BaseTestCase):
    url: str = reverse_lazy("login")
    template_name: str = "registration/login.html"

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, MyLoginView)

    # integration
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
