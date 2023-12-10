from pprint import pprint

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.test import Client

from apps.registration.forms import (
    RegistrationForm,
    ERROR_MESSAGE_USERNAME_LESS_THAN_3,
)
from apps.registration.views import (
    RegistrationView,
    REGISTRATION_SUCCESS_MESSAGE,
    MyLoginView,
    LOGIN_SUCCESS_MESSAGE,
)
from utils.tests.base import ExtendedTestCase

User = get_user_model()


class RegistrationViewTestCase(ExtendedTestCase):
    url: str = reverse_lazy("registration")
    view_class = RegistrationView

    class FormValid:
        redirect_url: str = reverse_lazy("login")

    class FormInvalid:
        template_name: str = "registration/register.html"

    # unittest
    def test_content_registration_form(self) -> None:
        request = self.request_factory.get(self.url)
        response = self.view_class.as_view()(request)

        self.assertIsInstance(
            response.context_data.get("form"),
            RegistrationForm,
        )

    # unittest
    def test_form_valid_redirect(self) -> None:
        request = self.request_factory.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
                "password2": "12345678",
            },
        )
        response = self.view_class.as_view()(request)
        response.client = Client()

        self.assertRedirects(response, self.FormValid.redirect_url)

    # integration
    def test_form_valid_creating_user(self) -> None:
        request = self.request_factory.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
                "password2": "12345678",
            },
        )
        response = self.view_class.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    # integration
    def test_form_invalid_no_users(self) -> None:
        request = self.request_factory.post(
            self.url,
            data={
                "username": "vl",
                "password": "12345678",
                "password2": "12345678",
            },
        )
        response = self.view_class.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    # integration
    def test_form_invalid_template(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "username": "vl",
                "password": "12345678",
                "password2": "12345678",
            },
        )

        self.assertTemplateUsed(response, self.FormInvalid.template_name)

    # integration
    def test_form_invalid_show_error(self) -> None:
        request = self.request_factory.post(
            self.url,
            data={
                "username": "vo",
                "password": "12345678",
                "password2": "12345678",
            },
        )
        response = self.view_class.as_view()(request)

        self.assertContains(response, ERROR_MESSAGE_USERNAME_LESS_THAN_3)

    # unittest
    def test_form_valid_success_message(self) -> None:
        request = self.request_factory.post(
            self.url,
            data={
                "username": "vlad",
                "password": "12345678",
                "password2": "12345678",
            },
        )
        self.view_class.as_view()(request)

        message = str(next(iter(get_messages(request))))
        self.assertEqual(
            message,
            REGISTRATION_SUCCESS_MESSAGE,
        )


class MyLoginViewTestCase(ExtendedTestCase):
    url: str = reverse_lazy("login")
    view_class = MyLoginView

    class FormValid:
        redirect_url: str = reverse_lazy("home:home")

    class FormInvalid:
        template_name: str = "registration/login.html"

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(username="vlad", password="12345678")

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

    # # integration
    # def test_form_valid_success_message(self) -> None:
    #     response = self.client.post(
    #         self.url,
    #         data={
    #             'username': 'vlad',
    #             'password': '12345678',
    #         }
    #     )
    #     message = str(next(iter(get_messages(response.request))))
    #     self.assertEqual(
    #         message,
    #         LOGIN_SUCCESS_MESSAGE,
    #     )
