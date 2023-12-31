import functools
from typing import Optional, Callable

from tests.registration.page import RegistrationPage


def register(
    _func: Optional[Callable] = None,
    *,
    username: str = "user",
    password: str = "12345678",
    path: str = "/registration",
) -> Callable:
    """
    A register decorator that allows you to already be registered during
    test running.
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            url = f"{self.live_server_url}{path}"

            reg_page = RegistrationPage(self.page.driver)

            reg_page.go_to_page(url)

            reg_page.register(
                username=username,
                password=password,
            )
            return func(self, *args, **kwargs)

        return inner

    return wrapper(_func) if _func else wrapper
