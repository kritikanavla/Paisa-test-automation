"""Selenium Base Page Object encapsulating common browser actions and explicit waits."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, List, Optional
import os
import time


class BasePage:
    """Base class for all Page Objects providing reusable interactions and robust waits."""

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def navigate_to(self, url: str) -> None:
        """Navigate to a specified URL."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the page title."""
        return self.driver.title

    def find(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be present in DOM and visible, then return it."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to exist in DOM (even if not visible yet)."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find all matching elements currently present."""
        return self.driver.find_elements(*locator)

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """Wait for element to be clickable and click it."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """Type text into an input element after ensuring visibility."""
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """Get visible text content of an element."""
        return self.find(locator, timeout=timeout).text.strip()

    def is_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if an element is visible within timeout seconds without raising TimeoutException."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is present in DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> Optional[str]:
        """Get attribute value of an element."""
        element = self.find(locator)
        return element.get_attribute(attribute)

    def save_screenshot(self, filename: str) -> str:
        """Capture and save a screenshot to disk."""
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        self.driver.save_screenshot(filename)
        return filename
