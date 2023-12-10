from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import get_messages
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy

from apps.registration.views import MyLoginView, LOGIN_SUCCESS_MESSAGE
from utils.tests.base import ExtendedTestCase

User = get_user_model()


class MyLoginViewTestCase(ExtendedTestCase):
    url: str = reverse_lazy("login")
    view_class = MyLoginView

    class FormValid:
        redirect_url: str = reverse_lazy("home:home")

    class FormInvalid:
        template_name: str = "registration/login.html"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="vlad",
            password="12345678",
        )

    def test_content_authentication_form(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vvvv",
                "password": "12345678",
            },
        )
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    # integration
    def test_form_valid_redirect(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
            },
        )
        self.assertRedirects(response, self.FormValid.redirect_url)

    # integration
    def test_form_valid_creating_one_session(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Session.objects.count(), 1)

    # integration
    def test_form_valid_success_message(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
            },
        )
        self.assertEqual(response.status_code, 302)

        message = str(next(iter(get_messages(response.wsgi_request))))
        self.assertEqual(
            message,
            LOGIN_SUCCESS_MESSAGE,
        )

    # integration
    def test_form_invalid_template(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vla",
                "password": "12345678",
            },
        )
        self.assertTemplateUsed(
            response,
            self.FormInvalid.template_name,
        )

    # integration
    def test_form_invalid_can_show_error(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vla",
                "password": "12345678",
            },
        )
        self.assertContains(
            response,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive.",
        )
