"""Page Object for Flow Tracker page on Paisa platform."""
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage
from config.config import Config


class FlowPage(BasePage):
    """Encapsulates locators and user interactions for Paisa authentication and Flow Tracker."""

    def __init__(self, page: Page):
        super().__init__(page, timeout=Config.DEFAULT_TIMEOUT * 1000)
        # Login Locators
        self.email_input: Locator = self.page.get_by_placeholder("Email address")
        self.password_input: Locator = self.page.get_by_placeholder("Password")
        self.signin_button: Locator = self.page.get_by_role("button", name="Sign In").last
        
        # Navigation & Flow Tracker Locators
        self.flow_tracker_link: Locator = self.page.get_by_role("link", name="Flow Tracker").first
        self.search_ticker_input: Locator = self.page.get_by_placeholder("Search ticker...")
        self.flow_tracker_header: Locator = self.page.get_by_role("heading", name="Institutional Flow Tracker").or_(self.page.get_by_text("Flow Tracker")).first

    def load_login_page(self) -> "FlowPage":
        """Navigate to Login page."""
        self.navigate_to(Config.LOGIN_URL)
        return self

    def login(self, email: str = Config.VALID_EMAIL, password: str = Config.VALID_PASSWORD) -> "FlowPage":
        """Perform user authentication."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.signin_button.click()
        self.wait_for_timeout(500)
        return self

    def navigate_to_flow_tracker(self) -> "FlowPage":
        """Click body and navigate to Flow Tracker section."""
        self.page.locator("body").click()
        self.flow_tracker_link.click(force=True)
        self.page.locator("body").click()
        self.wait_for_timeout(5000)
        return self

    def search_ticker(self, ticker: str) -> "FlowPage":
        """Search for stock ticker in Flow Tracker."""
        self.page.locator("body").click()
        self.search_ticker_input.click(force=True)
        self.search_ticker_input.fill(ticker)
        self.press_key("Enter")
        self.wait_for_timeout(5000)
        self.page.locator("body").click()
        self.wait_for_timeout(5000)
        return self



    def is_ticker_heading_visible(self, ticker: str) -> bool:
        """Verify if ticker symbol heading is displayed on the page."""
        return self.page.get_by_text(ticker.upper(), exact=True).first.is_visible()


