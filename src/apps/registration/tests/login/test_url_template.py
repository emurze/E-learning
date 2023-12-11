from django.urls import reverse_lazy, resolve

from apps.registration.views import MyLoginView
from utils.tests.base import BaseTestCase


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
