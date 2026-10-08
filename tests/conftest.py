"""Pytest fixtures for browser setup, teardown, and screenshot capture on failure."""
import pytest
import os
import sys
import datetime
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config
from pages.flow_page import FlowPage


@pytest.fixture(scope="function")
def playwright_page(request):
    """Playwright Page fixture with automatic screenshot capture on failure."""
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=Config.HEADLESS, slow_mo=500 if not Config.HEADLESS else 0)
        context: BrowserContext = browser.new_context(
            viewport={"width": Config.WINDOW_WIDTH, "height": Config.WINDOW_HEIGHT}
        )
        page: Page = context.new_page()
        
        yield page
        
        # Capture screenshot if test failed
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            file_path = os.path.join(screenshot_dir, f"{request.node.name}_{timestamp}.png")
            page.screenshot(path=file_path, full_page=True)
            print(f"\n[Playwright Failure Screenshot saved]: {file_path}")
            
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def flow_page(playwright_page) -> FlowPage:
    """Fixture providing initialized FlowPage object."""
    return FlowPage(playwright_page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to record test status for fixture conditional cleanup or screenshots."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
