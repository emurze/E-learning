from tests.base.shared import SharedTestCase


class HomePage:
    def __init__(self, test: SharedTestCase) -> None:
        self.driver = test.driver

    def get_title(self) -> None:
        return self.driver.title
