from django.urls import reverse_lazy, resolve

from apps.registration.views import MyLogoutView
from utils.tests.base import BaseTestCase


class MyLogoutViewIntegrationTest(BaseTestCase):
    url: str = reverse_lazy("logout")

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, MyLogoutView)
