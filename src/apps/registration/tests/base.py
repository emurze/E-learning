from django.test import TestCase, RequestFactory


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()
