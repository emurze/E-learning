import time

from tests.login.page import LoginPage
from tests.shared.driver import get_driver
from tests.shared.testcase import EndToEndTestCase


class LoginTestCase(EndToEndTestCase):
    page_class = LoginPage
    path: str = "/login"
    port: int = 8082

    def test_title(self) -> None:
        # Client comes to Login page
        self.page.go_to_page(self.url)

        # And wants to see Log-in title
        self.assertEqual(self.page.title, 'Log-in')

    # def test_form_can_show_success(self) -> None:
    #     # Client wises to fill and send the form
    #     self.page.go_to_page(self.live_server_url + '/registration')
    #
    #     username_input = self.page.find_element(By.ID, 'id_username')
    #     password_input = self.page.find_element(By.ID, 'id_password')
    #     password2_input = self.page.find_element(By.ID, 'id_password2')
    #
    #     username_input.send_keys('vlad')
    #     password_input.send_keys('12345678')
    #     password2_input.send_keys('12345678')
    #     password2_input.submit()
    #
    #     # Client input correct data
    #     self.page.enter_username('vlad')
    #     self.page.enter_password('12345678')
    #     self.page.submit()
    #
    #     # Client wants to see E-Learning page
    #     self.assertEqual(self.page.title, "E-Learning")
    #
    #     # And wants to see success message
    #     success_message = self.page.get_success_message()
    #     self.assertIn("Authorization has been successful", success_message)
