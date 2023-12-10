from tests.login.page import LoginPage
from tests.registration.decorators import register
from tests.shared.testcase import EndToEndTestCase


class LoginTestCase(EndToEndTestCase):
    page_class = LoginPage
    path: str = "/login"
    port: int = 8082

    def test_title(self) -> None:
        # Client comes to Login page
        self.page.go_to_page(self.url)

        # And wants to see Log-in title
        self.assertEqual(self.page.title, "Log-in")

    @register(username="vlad", password="12345678")
    def test_form_can_show_success(self) -> None:
        # After registration, client wises to be redirected to Log-in page
        self.assertEqual(self.page.title, "Log-in")

        # Client input correct data
        self.page.enter_username("vlad")
        self.page.enter_password("12345678")
        self.page.submit()

        # Client wants to see E-Learning page
        self.assertEqual(self.page.title, "E-Learning")

        # And wants to see success message
        success_message = self.page.get_success_message()
        self.assertIn("Authorization has been successful", success_message)
