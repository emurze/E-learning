from functools import lru_cache

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from tests.shared.page import BasePage


class LoginPage(BasePage):
    @lru_cache(maxsize=16)
    def _get_password(self) -> WebElement:
        return self.find_element(By.ID, "id_password")

    def enter_username(self, username: str) -> None:
        username_input = self.find_element(By.ID, "id_username")
        username_input.send_keys(username)

    def enter_password(self, password: str) -> None:
        password_input = self._get_password()
        password_input.send_keys(password)

    def submit(self) -> None:
        password_input = self._get_password()
        password_input.submit()

    def get_success_message(self) -> str:
        return self.find_element(By.CLASS_NAME, "success").text
