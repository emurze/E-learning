from selenium.webdriver.common.by import By

from tests.base.shared import SharedTestCase
from tests.registration.page import RegistrationPage


class RegistrationPageTestCase(SharedTestCase):
    page_title: str = 'Registration'

    @property
    def url(self) -> str:
        return f'{self.live_server_url}/registration'

    def setUp(self) -> None:
        super().setUp()

        # Client comes to the page
        self.driver.get(self.url)
        self.page = RegistrationPage(self)

    def test_can_show_title(self) -> None:
        # Client wants to see Registration title
        self.assertEqual(self.page.get_title(), self.page_title)

    def test_form_valid_redirect(self) -> None:
        # Client wants to see form
        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        password2_input = self.driver.find_element(By.ID, 'id_password2')

        # Client wise to fill form
        username_input.send_keys('user_1')
        password_input.send_keys('12345678')
        password2_input.send_keys('12345678')
        password2_input.submit()
