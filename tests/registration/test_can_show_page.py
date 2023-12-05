from tests.base.shared import SharedTestCase
from tests.registration.page import RegistrationPage


class CanShowPageTest(SharedTestCase):
    page_title: str = 'Registration'

    def test_show_title(self) -> None:
        self.driver.get(f'{self.live_server_url}/registration')

        page = RegistrationPage(self)

        self.assertEqual(page.get_title(), self.page_title)
