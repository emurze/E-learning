from typing import Type
from unittest import skip

from selenium.webdriver.common.by import By

from tests.login.page import LoginPage
from tests.shared.testcase import SharedTestCase


class LoginTestCase(SharedTestCase):
    page_class: Type[LoginPage] = LoginPage
    path: str = "/login"

    # def test_title(self) -> None:
    #     self.driver.get(self.url)
    #     self.assertEqual(self.page.get_title(), 'Log-in')

    # @skip
    # def test_form_can_show_success(self) -> None:
    #     self.driver.get(self.url)
    #
    #     username = self.driver.find_element(By.ID, "id_username")
    #     password = self.driver.find_element(By.ID, "id_password")
    #
    #     # Client input correct data
    #     username.send_keys("user_1")
    #     password.send_keys("12345678")
    #     password.submit()
    #
    #     # And want to see success message
    #     success = self.driver.find_element(By.CLASS_NAME, "success")
    #     self.assertIn("hi", success.text)
