from .driver import get_driver
from .live_server import MyLiveServerTestCase


class SharedTestCase(MyLiveServerTestCase):
    def setUp(self) -> None:
        self.driver = get_driver()
