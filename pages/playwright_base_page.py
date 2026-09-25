"""Playwright Base Page Object providing unified interactions and assertions."""
from playwright.sync_api import Page, Locator, expect
from typing import Optional
import os


class PlaywrightBasePage:
    """Base class for Playwright Page Objects with auto-waiting and assertion support."""

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.page.set_default_timeout(self.timeout)

    def navigate_to(self, url: str) -> None:
        """Navigate to URL and wait until network is idle / DOM loaded."""
        self.page.goto(url, wait_until="domcontentloaded")

    def get_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def take_screenshot(self, filepath: str) -> str:
        """Capture screenshot to path."""
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        self.page.screenshot(path=filepath, full_page=True)
        return filepath
