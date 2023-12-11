import functools
from typing import Optional, Callable

from tests.login.page import LoginPage


def login(
    _func: Optional[Callable] = None,
    *,
    username: str = "user",
    password: str = "12345678",
    path: str = "/login",
) -> Callable:
    """
    A login decorator that allows you to already be logged in during test
    running.
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            url = f"{self.live_server_url}{path}"

            login_page = LoginPage(self.page.driver)

            login_page.go_to_page(url)

            login_page.login(
                username=username,
                password=password,
            )
            return func(self, *args, **kwargs)

        return inner

    return wrapper(_func) if _func else wrapper
