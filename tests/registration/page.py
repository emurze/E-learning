from tests.shared.page import BasePage


class RegistrationPage(BasePage):
    def get_title(self) -> str:
        return self.driver.title
