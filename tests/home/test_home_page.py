from typing import Type

from tests.home.page import HomePage
from tests.shared.testcase import SharedTestCase


class HomePageTestCase(SharedTestCase):
    page_class: Type[HomePage] = HomePage
    path: str = ''

    def test_title(self) -> None:
        self.driver.get(self.url)
        self.assertEqual(self.page.get_title(), "E-Learning")
