import sys
import os

# Add project root directory to sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.base_page import BasePage
from config.config import Config
# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto(Config.LOGIN_URL)
    
    # Fill in credentials loaded automatically from .env via Config
    page.get_by_placeholder("Email address").fill(Config.VALID_EMAIL)
    page.get_by_placeholder("Password").fill(Config.VALID_PASSWORD)
    
    # Click Sign In button
    page.get_by_role("button", name="Sign In").last.click()
    
    page.locator("body").click()
    page.get_by_placeholder("Search ticker...").fill("amazon")
    page.keyboard.press("Enter")
    page.wait_for_timeout(10000)
    page.locator("body").click()



