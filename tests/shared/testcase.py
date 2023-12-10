import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .driver import get_driver
from .exceptions import PageDoesNotExistsError


class BaseLiveServerTestCase(StaticLiveServerTestCase):
    """
    Require:
        - port: int, between 8081 - 8999 like 8081
    """
    host = socket.gethostbyname(socket.gethostname())


class EndToEndTestCase(BaseLiveServerTestCase):
    """The best TestCase for End-To-End functionality"""

    port: int = 0  # -> server launch

    page_class = None  # -> self.page

    path: str = ""  # -> self.url

    @property
    def url(self) -> str:
        return f"{self.live_server_url}{self.path}"

    def setUp(self) -> None:
        if self.page_class is None:
            raise PageDoesNotExistsError('Please add page_class attribute')

        self.page = self.page_class(get_driver())

    def tearDown(self) -> None:
        self.page.quit()
