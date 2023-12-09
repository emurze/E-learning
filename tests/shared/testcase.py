from .driver import get_driver
from .live_server import MyLiveServerTestCase


class SharedTestCase(MyLiveServerTestCase):
    """
    Base test case for shared functionality.

    Attributes:
        page_class: Type[BasePage], allows you to use initiated self.page
        path: str, allows you to use self.url
    """

    page_class = None
    path: str = ""

    @property
    def url(self) -> str:
        return f"{self.live_server_url}{self.path}"

    def setUp(self) -> None:
        self.driver = get_driver()

        if self.page_class is not None:
            self.page = self.page_class(self)

    def tearDown(self) -> None:
        self.driver.quit()
