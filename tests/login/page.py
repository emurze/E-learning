from tests.shared.page import BasePage


class LoginPage(BasePage):
    def get_title(self) -> str:
        return self.driver.title
