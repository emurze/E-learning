from collections.abc import Generator

from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory


class RequestFactoryExtendedAdapter(RequestFactory):
    """
    RequestFactory Adapter that add MessageMiddleware

    Task: Refactor using metaprogramming
    """

    def get(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().get(*args, **kwargs))

    def post(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().post(*args, **kwargs))

    def head(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().head(*args, **kwargs))

    def trace(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().trace(*args, **kwargs))

    def options(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().options(*args, **kwargs))

    def put(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().put(*args, **kwargs))

    def patch(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().patch(*args, **kwargs))

    def delete(self, *args, **kwargs) -> WSGIRequest:
        return self.setup(super().delete(*args, **kwargs))

    def setup(self, request: WSGIRequest) -> WSGIRequest:
        methods = list(self._find_all_setup_methods())
        request = self._apply_methods(request, methods)
        return request

    def _find_all_setup_methods(self) -> Generator:
        for x in dir(self):
            if x.startswith("setup_") and callable(item := getattr(self, x)):
                yield item

    @staticmethod
    def _apply_methods(request: WSGIRequest, methods: list) -> WSGIRequest:
        while methods:
            method = methods.pop()
            request = method(request)
        return request

    @staticmethod
    def setup_dont_enforce_csrf_checks(request: WSGIRequest) -> WSGIRequest:
        setattr(request, "_dont_enforce_csrf_checks", True)
        return request

    @staticmethod
    def setup_message_middleware(request: WSGIRequest) -> WSGIRequest:
        setattr(request, "session", "session")
        setattr(request, "_messages", FallbackStorage(request))
        return request
