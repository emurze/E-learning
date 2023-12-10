import abc
import os

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class BaseDriverFactory(abc.ABC):
    @abc.abstractmethod
    def get_webdriver(self) -> WebDriver: ...


class FirefoxDriverFactory(BaseDriverFactory):
    host = os.getenv("STAGING_SERVER", "firefox")
    port = "4444"

    @classmethod
    def get_webdriver(cls) -> WebDriver:
        options = webdriver.FirefoxOptions()
        return webdriver.Remote(
            f"http://{cls.host}:{cls.port}",
            options=options,
        )


class ChromeDriverFactory(BaseDriverFactory):
    host = os.getenv("STAGING_SERVER", "chrome")
    port = "4444"

    @classmethod
    def get_webdriver(cls) -> WebDriver:
        options = webdriver.ChromeOptions()
        return webdriver.Remote(
            f"http://{cls.host}:{cls.port}",
            options=options,
        )


def get_driver() -> WebDriver:
    """Driver Factory"""
    return ChromeDriverFactory.get_webdriver()
