from tests.home.page import HomePage
from tests.shared.decorators import authorization
from tests.shared.testcase import EndToEndTestCase


class HomePageTestCase(EndToEndTestCase):
    page_class = HomePage
    path: str = "/"
    port: int = 8083

    @authorization
    def test_title(self) -> None:
        # Client comes to E-Learning page
        self.page.go_to_page(self.url)

        # And wants to see E-Learning title
        self.assertEqual(self.page.title, "E-Learning")
