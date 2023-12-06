from django.urls import resolve, reverse_lazy

from apps.home.views import HomeView
from utils.tests.base import BaseTestCase


class HomeViewTestCase(BaseTestCase):
    url: str = reverse_lazy("home:home")
    template_name: str = "home/home.html"

    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, HomeView)

    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
