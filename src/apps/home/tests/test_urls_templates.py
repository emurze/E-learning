from django.urls import resolve, reverse_lazy

from apps.home.views import HomeView
from utils.tests.base import LoginBaseTestCase


class HomeViewTestCase(LoginBaseTestCase):
    url: str = reverse_lazy("home:home")
    template_name: str = "home/home.html"

    # integration
    def test_url(self) -> None:
        resolver = resolve(self.url)
        self.assertEqual(resolver.func.view_class, HomeView)

    # integration
    def test_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)
