"""End-to-End Test Suite for Flow Tracker on Paisa platform."""
import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from playwright.sync_api import sync_playwright, expect
from config.config import Config
from pages.flow_page import FlowPage


@pytest.mark.playwright
def test_flow_tracker_navigation(flow_page: FlowPage):
    """E2E Test 1: User login and successful navigation to Flow Tracker module."""
    flow_page.load_login_page()
    flow_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)
    flow_page.navigate_to_flow_tracker()
    
    # Assert Flow Tracker link is visible
    expect(flow_page.flow_tracker_link).to_be_visible()


@pytest.mark.playwright
def test_flow_tracker_search_ticker(flow_page: FlowPage):
    """E2E Test 2: Search ticker functionality (e.g. AMZN) in Flow Tracker."""
    flow_page.load_login_page()
    flow_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)
    flow_page.navigate_to_flow_tracker()
    
    # Perform Ticker search for AMZN
    flow_page.search_ticker("amzn")
    
    # Assert AMZN heading is displayed upon search
    assert flow_page.is_ticker_heading_visible("AMZN")


@pytest.mark.playwright
def test_flow_tracker_multiple_ticker_search(flow_page: FlowPage):
    """E2E Test 3: Search multiple stock tickers sequentially (AAPL, NVDA)."""
    flow_page.load_login_page()
    flow_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)
    flow_page.navigate_to_flow_tracker()
    
    for ticker in ["aapl", "nvda"]:
        flow_page.search_ticker(ticker)
        assert flow_page.is_ticker_heading_visible(ticker)


if __name__ == "__main__":
    print("Running Flow Tracker standalone script execution...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS, slow_mo=500)
        context = browser.new_context(viewport={"width": Config.WINDOW_WIDTH, "height": Config.WINDOW_HEIGHT})
        page = context.new_page()
        
        flow = FlowPage(page)
        flow.load_login_page()
        flow.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)
        flow.navigate_to_flow_tracker()
        flow.search_ticker("amzn")
        
        print("Flow Tracker standalone script completed successfully!")
        context.close()
        browser.close()
