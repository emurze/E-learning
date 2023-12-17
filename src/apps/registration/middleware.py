import logging
from collections.abc import Callable

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect

lg = logging.getLogger(__name__)


class LoginRequiredMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.open_urls = getattr(settings, "OPEN_URLS", [])

    def __call__(self, request: WSGIRequest) -> HttpResponse:
        """
        If user is not authenticated, and it's not opened page
        then
            redirect to login page with saved path to the previous page
        """

        url = request.path_info
        user_is_not_authenticated = not request.user.is_authenticated

        if user_is_not_authenticated and url not in self.open_urls:
            return redirect(f"{self.login_url}?next={request.path}")

        return self.get_response(request)
