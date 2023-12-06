from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from unittest.mock import Mock, patch, MagicMock

from apps.registration.middleware import LoginRequiredMiddleware
from utils.tests.base import BaseTestCase

User = get_user_model()


class LoginRequiredMiddlewareTestCase(BaseTestCase):
    open_url: str = "hi"

    # unittest
    @patch("apps.registration.middleware.redirect")
    def test_redirect_when_user_is_not_authenticated(
        self, mock_redirect: MagicMock
    ) -> None:
        get_response = Mock()
        request = self.request_factory.get("/")
        request.user = AnonymousUser()

        middleware = LoginRequiredMiddleware(get_response)
        middleware(request)

        redirect_path = mock_redirect.call_args[0][0]

        self.assertFalse(get_response.called)
        self.assertTrue(redirect_path.startswith(settings.LOGIN_URL))

    # integration
    def test_getting_response(self) -> None:
        get_response = Mock()
        request = self.request_factory.get("/")
        request.user = User.objects.create_user(
            username="vlad",
            password="12345678",
        )

        middleware = LoginRequiredMiddleware(get_response)
        response = middleware(request)

        self.assertTrue(get_response.called)
        self.assertEqual(response, get_response(request))

    # unittest
    @patch("apps.registration.middleware.settings")
    def test_getting_response_when_user_is_not_authenticated_and_open_url(
        self, mock_settings: MagicMock
    ) -> None:
        get_response = Mock()

        mock_settings.OPEN_URLS = [self.open_url]

        request = self.request_factory.get(self.open_url)
        request.user = AnonymousUser()

        middleware = LoginRequiredMiddleware(get_response)
        response = middleware(request)

        self.assertEqual(response, get_response(request))
