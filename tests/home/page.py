from tests.shared.page import BasePage


class HomePage(BasePage):
    def get_title(self) -> str:
        return self.driver.title
