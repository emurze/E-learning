from tests.registration.decorators import register
from tests.registration.page import RegistrationPage
from tests.shared.testcase import EndToEndTestCase


class RegistrationPageTestCase(EndToEndTestCase):
    page_class = RegistrationPage
    path: str = "/registration"
    port = 8081

    def test_title(self) -> None:
        # Client comes to Registration page
        self.page.go_to_page(self.url)

        # And wants to see Registration title
        self.assertEqual(self.page.title, "Registration")

    @register
    def test_can_see_success_message(self) -> None:
        # After registration, client wants to see a success message
        success_message = self.page.get_success_message()
        self.assertIn("Registration has been successful", success_message)
