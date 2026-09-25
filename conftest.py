"""Pytest fixtures for browser setup, teardown, and screenshot capture on failure."""
import pytest
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.config import Config


@pytest.fixture(scope="session")
def browser_options():
    """Configure Chrome options for Selenium."""
    options = Options()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    return options


@pytest.fixture(scope="function")
def driver(browser_options, request):
    """Selenium WebDriver fixture with automatic screenshot on failure."""
    service = Service(ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service, options=browser_options)
    driver_instance.implicitly_wait(0)  # Use explicit waits in POM
    
    yield driver_instance
    
    # Capture screenshot if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        file_path = os.path.join(screenshot_dir, f"{request.node.name}_{timestamp}.png")
        driver_instance.save_screenshot(file_path)
        print(f"\n[Selenium Failure Screenshot saved]: {file_path}")
        
    driver_instance.quit()


@pytest.fixture(scope="function")
def playwright_page(request):
    """Playwright Page fixture with automatic screenshot on test failure."""
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=Config.HEADLESS)
        context: BrowserContext = browser.new_context(
            viewport={"width": Config.WINDOW_WIDTH, "height": Config.WINDOW_HEIGHT}
        )
        page: Page = context.new_page()
        
        yield page
        
        # Capture screenshot on failure
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            file_path = os.path.join(screenshot_dir, f"{request.node.name}_{timestamp}.png")
            page.screenshot(path=file_path, full_page=True)
            print(f"\n[Playwright Failure Screenshot saved]: {file_path}")
            
        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status for fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
