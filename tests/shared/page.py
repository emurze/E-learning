from dataclasses import dataclass
from typing import TypeAlias

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

WebElements: TypeAlias = list[WebElement]


@dataclass(frozen=True, eq=True)
class BasePage:
    driver: WebDriver

    @property
    def title(self) -> str:
        return self.driver.title

    def find_element(self, by: str, value, time: int = 10) -> WebElement:
        return WebDriverWait(self.driver, time).until(
            ec.presence_of_element_located((by, value)),
            message=f"Can't find element by locator {(by, value)}",
        )

    def find_elements(self, by: str, value, time: int = 10) -> WebElements:
        return WebDriverWait(self.driver, time).until(
            ec.presence_of_all_elements_located((by, value)),
            message=f"Can't find elements by locator {(by, value)}",
        )

    def quit(self):
        self.driver.quit()

    def go_to_page(self, url: str) -> None:
        self.driver.get(url)
