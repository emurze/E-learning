import logging

from apps.registration.forms import (
    RegistrationForm,
    ERROR_MESSAGE_PASSWORD_LESS_THAN_7,
    ERROR_MESSAGE_USERNAME_LESS_THAN_3,
    ERROR_MESSAGE_PASSWORDS_DO_NOT_EQUALLY,
)
from utils.tests.base import BaseTestCase

lg = logging.getLogger(__name__)


class RegistrationFormTest(BaseTestCase):
    def test_error_username_less_than_3(self) -> None:
        form = RegistrationForm(data={
            'username': 'vl',
            'password': 12345678,
            'password2': 12345678,
        })
        self.assertIn(
            ERROR_MESSAGE_USERNAME_LESS_THAN_3,
            form.errors['username'],
        )

    def test_error_passwords_do_not_equally(self) -> None:
        form = RegistrationForm(data={
            'username': 'vlad',
            'password': 12345678,
            'password2': 123456789,
        })
        self.assertIn(
            ERROR_MESSAGE_PASSWORDS_DO_NOT_EQUALLY,
            form.errors['password2'],
        )

    def test_error_password_less_than_7(self) -> None:
        form = RegistrationForm(data={
            'username': 'vlad',
            'password': 1234567,
            'password2': 1234567,
        })
        self.assertIn(
            ERROR_MESSAGE_PASSWORD_LESS_THAN_7,
            form.errors['password2'],
        )
