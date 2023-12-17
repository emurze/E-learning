import functools
from typing import Optional, Callable

from tests.login.page import LoginPage
from tests.registration.page import RegistrationPage


def authorization(
    _func: Optional[Callable] = None,
    *,
    username: str = "user",
    password: str = "12345678",
    registration_path: str = "/registration",
) -> Callable:
    """
    An authorization decorator that allows you to already be logged in during
    test running.
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            reg_url = f"{self.live_server_url}{registration_path}"

            reg_page = RegistrationPage(self.page.driver)

            reg_page.go_to_page(reg_url)

            reg_page.register(
                username=username,
                password=password,
            )

            log_page = LoginPage(self.page.driver)
            log_page.login(
                username=username,
                password=password,
            )
            return func(self, *args, **kwargs)

        return inner

    return wrapper(_func) if _func else wrapper
