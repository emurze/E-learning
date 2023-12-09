from unittest.mock import Mock

from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.views.generic import FormView

from apps.registration.mixins import SuccessMessageMixin

from utils.tests.base import BaseTestCase


class SuccessMessageMixinTestCase(BaseTestCase):
    class View(SuccessMessageMixin, FormView):
        success_message: str = 'Registration has been successful'
        template_name: str = 'registration/login.html'
        form_class: Mock = Mock()
        success_url: Mock = Mock()

        def form_valid(self, form: Mock) -> dict:
            super().form_valid(form)
            return self.form_invalid(form)

    def setUp(self):
        super().setUp()
        self.request = self.request_factory.post('/')
        setattr(self.request, 'session', 'session')
        setattr(self.request, '_messages', FallbackStorage(self.request))

    # unittest
    def test_context_data_success_message(self) -> None:
        self.View.as_view()(self.request)
        message = str(
            next(
                iter(get_messages(self.request))
            )
        )
        self.assertEqual(message, self.View.success_message)
