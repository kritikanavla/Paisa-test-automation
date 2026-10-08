"""Base Page Object for Playwright automation framework."""
from playwright.sync_api import Page, Locator, expect
from typing import Optional
import os


class BasePage:
    """Base class for all Page Objects providing reusable Playwright interactions."""

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.page.set_default_timeout(self.timeout)

    def navigate_to(self, url: str) -> None:
        """Navigate to a target URL."""
        self.page.goto(url, wait_until="domcontentloaded")

    def get_url(self) -> str:
        """Get current browser URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get current page title."""
        return self.page.title()

    def click(self, selector_or_locator) -> None:
        """Click an element using string selector or Locator instance."""
        if isinstance(selector_or_locator, str):
            self.page.locator(selector_or_locator).click()
        else:
            selector_or_locator.click()

    def fill(self, selector_or_locator, value: str) -> None:
        """Fill input field with text."""
        if isinstance(selector_or_locator, str):
            self.page.locator(selector_or_locator).fill(value)
        else:
            selector_or_locator.fill(value)

    def press_key(self, key: str) -> None:
        """Press a keyboard key."""
        self.page.keyboard.press(key)

    def wait_for_timeout(self, timeout_ms: int) -> None:
        """Wait for specified milliseconds."""
        self.page.wait_for_timeout(timeout_ms)

    def take_screenshot(self, filepath: str) -> str:
        """Capture page screenshot."""
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        self.page.screenshot(path=filepath, full_page=True)
        return filepath
