from tests.base.shared import SharedTestCase


class HomePageTestCase(SharedTestCase):
    @property
    def url(self) -> str:
        return f"{self.live_server_url}"

    def test_title(self) -> None:
        self.driver.get(self.url)
        self.assertEqual(self.driver.title, "E-Learning")
