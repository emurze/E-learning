from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.db.models import Model, QuerySet
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from utils import mixin_for
from utils.tests.request_factory_extended_adapter import (
    RequestFactoryExtendedAdapter,
)

User = get_user_model()


class LoginMixin(mixin_for(TestCase)):
    """Mixin for TestCase"""

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
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_NAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
        cls.site = AdminSite()

    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    @staticmethod
    def make_url(site: AdminSite, model: type[Model], page: str, *args) -> str:
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        return reverse(
            f"{site.name}:{app_label}_{model_name}_{page}",
            args=args,
        )

    @staticmethod
    def get_queryset(response: TemplateResponse) -> QuerySet:
        return response.context_data["cl"].queryset


class ExtendedTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactoryExtendedAdapter()


class LoginBaseTestCase(LoginMixin, BaseTestCase):
    """BaseTestCase with LoginMixin"""


class LoginExtendedTestCase(LoginMixin, ExtendedTestCase):
    """ExtendedTestCase with LoginMixin"""
