from django.contrib.sessions.models import Session
from django.urls import reverse_lazy

from apps.registration.views import MyLogoutView
from utils.tests.base import LoginBaseTestCase


class MyLogoutViewTestCase(LoginBaseTestCase):
    url: str = reverse_lazy("logout")
    view_class = MyLogoutView
    redirect_url: str = reverse_lazy("login")

    # integration
    def test_redirect(self) -> None:
        # Client sees page because it's authenticated
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # Client logouts
        response = self.client.get(self.url)

        # And it should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertIn("login/", response.url)

        # And it doesn't see page because it isn't authenticated
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    # integration
    def test_session_deletion(self) -> None:
        self.assertEqual(Session.objects.count(), 1)

        self.client.get(self.url)

        self.assertEqual(Session.objects.count(), 0)
