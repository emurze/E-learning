from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from utils import mixin_for
from utils.tests.request_factory_extended_adapter import (
    RequestFactoryExtendedAdapter,
)

User = get_user_model()


class LoginMixin(mixin_for(TestCase)):
    login_username: str = "vladik"
    login_password: str = "12345678"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username=cls.login_username,
            password=cls.login_password,
        )

    def setUp(self) -> None:
        self.client.login(
            username=self.login_username,
            password=self.login_password,
        )
        super().setUp()


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()


class ExtendedTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactoryExtendedAdapter()


class LoginBaseTestCase(LoginMixin, BaseTestCase):
    """
    BaseTestCase with your user or default:
        login_username: str
        login_password: str
    """


class LoginExtendedTestCase(LoginMixin, ExtendedTestCase):
    """
    ExtendedTestCase with your user or default:
        login_username: str
        login_password: str
    """
