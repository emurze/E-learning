from tests.base.shared import SharedTestCase


class RegistrationPage:
    def __init__(self, test: SharedTestCase) -> None:
        self.driver = test.driver

    def get_title(self) -> str:
        return self.driver.title
