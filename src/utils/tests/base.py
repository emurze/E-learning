from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
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


class AdminTestCase(BaseTestCase):
    model_name: str  # to apply permissions for access

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_user(
            username=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
            is_staff=True,
        )
        change_permission = Permission.objects.get(codename=f"change_{self.model_name}")
        self.user.user_permissions.add(change_permission)


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
