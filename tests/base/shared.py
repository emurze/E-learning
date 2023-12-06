from .driver import get_driver
from .live_server import MyLiveServerTestCase


class SharedTestCase(MyLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = get_driver()

    def tearDown(self) -> None:
        self.driver.quit()
