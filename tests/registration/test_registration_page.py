from typing import Type

from selenium.webdriver.common.by import By

from tests.registration.page import RegistrationPage
from tests.shared.testcase import SharedTestCase


class RegistrationPageTestCase(SharedTestCase):
    page_title: str = "Registration"
    page_class: Type[RegistrationPage] = RegistrationPage
    path: str = "/registration"

    def test_can_show_title(self) -> None:
        # Client comes to the page
        self.driver.get(self.url)

        # Client wants to see Registration title
        self.assertEqual(self.page.get_title(), self.page_title)
    #
    # def test_form_valid_redirect(self) -> None:
    #     # Client comes to the page
    #     self.driver.get(self.url)
    #
    #     # Client wants to see form
    #     username_input = self.driver.find_element(By.ID, "id_username")
    #     password_input = self.driver.find_element(By.ID, "id_password")
    #     password2_input = self.driver.find_element(By.ID, "id_password2")
    #
    #     # Client wises to fill form
    #     username_input.send_keys("user_1")
    #     password_input.send_keys("12345678")
    #     password2_input.send_keys("12345678")
    #     password2_input.submit()
    #
    #     # Then wants to be redirected to Log-in page
    #     self.assertEqual(self.driver.title, "Log-in")
    #
    #     # And wants to see the success message
    #     success = self.driver.find_element(By.CLASS_NAME, "success")
    #     self.assertIn("hi", success.text)
