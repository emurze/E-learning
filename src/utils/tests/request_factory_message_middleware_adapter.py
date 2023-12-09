from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory


class RequestFactoryMessageMiddlewareAdapter(RequestFactory):
    """
    RequestFactory Adapter that add MessageMiddleware

    Task: Refactor using metaprogramming
    """

    def get(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().get(*args, **kwargs))

    def post(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().post(*args, **kwargs))

    def head(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().head(*args, **kwargs))

    def trace(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().trace(*args, **kwargs))

    def options(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().options(*args, **kwargs))

    def put(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().put(*args, **kwargs))

    def patch(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().patch(*args, **kwargs))

    def delete(self, *args, **kwargs) -> WSGIRequest:
        return self.setup_message_middleware(super().delete(*args, **kwargs))

    @staticmethod
    def setup_message_middleware(request: WSGIRequest) -> WSGIRequest:
        setattr(request, "session", "session")
        setattr(request, "_messages", FallbackStorage(request))
        return request
