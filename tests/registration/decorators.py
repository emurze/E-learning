import functools
from collections.abc import Callable
from typing import Optional

from tests.registration.page import RegistrationPage


def register(
    _func: Optional[Callable] = None,
    *,
    username: str = "user",
    password: str = "12345678",
) -> Callable:
    """
    A registration decorator that allows you to already be registered during
    test writing.
    """

    def wrapper(func: Callable) -> Callable:
        path: str = "/registration"

        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            # Setup
            url = f"{self.live_server_url}{path}"
            reg_page = RegistrationPage(self.page.driver)

            # Client goes to the registration page
            reg_page.go_to_page(url)

            # And fill definite credentials
            reg_page.enter_username(username)
            reg_page.enter_password(password)
            reg_page.enter_password2(password)
            reg_page.submit()

            return func(self, *args, **kwargs)

        return inner

    return wrapper(_func) if _func else wrapper
