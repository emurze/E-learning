from tests.shared.testcase import SharedTestCase


class BasePage:
    def __init__(self, test: SharedTestCase) -> None:
        self.driver = test.driver
