from django.test import TestCase, RequestFactory

from .request_factory_message_middleware_adapter import (
    RequestFactoryMessageMiddlewareAdapter
)


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()


class ExtendedTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactoryMessageMiddlewareAdapter()
