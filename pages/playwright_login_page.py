"""Playwright Page Object for Paisa Login."""
from playwright.sync_api import Page, Locator, expect
from pages.playwright_base_page import PlaywrightBasePage
from config.config import Config


class PlaywrightLoginPage(PlaywrightBasePage):
    """Encapsulates locators and interactions for the Paisa Login page using Playwright."""

    def __init__(self, page: Page):
        super().__init__(page, timeout=Config.DEFAULT_TIMEOUT * 1000)
        self.email_input: Locator = self.page.locator("input#email")
        self.password_input: Locator = self.page.locator("input#password")
        self.submit_button: Locator = self.page.locator("button[type='submit']")
        self.signin_tab: Locator = self.page.locator("button").filter(has_text="Sign In").first
        self.register_tab: Locator = self.page.locator("button").filter(has_text="Register").first
        self.error_alert: Locator = self.page.locator("div.text-red-500, div:has-text('Invalid email or password.')").first
        self.welcome_heading: Locator = self.page.locator("text='Welcome to Paisa'")
        self.sub_heading: Locator = self.page.locator("text='Intelligent Financial Analysis Platform'")

    def load(self) -> "PlaywrightLoginPage":
        """Navigate to Login page."""
        self.navigate_to(Config.LOGIN_URL)
        return self

    def enter_email(self, email: str) -> "PlaywrightLoginPage":
        """Fill in email address."""
        self.email_input.fill(email)
        return self

    def enter_password(self, password: str) -> "PlaywrightLoginPage":
        """Fill in password."""
        self.password_input.fill(password)
        return self

    def click_sign_in_button(self) -> "PlaywrightLoginPage":
        """Click submit button."""
        self.submit_button.click()
        return self

    def login(self, email: str, password: str) -> "PlaywrightLoginPage":
        """Full login flow."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in_button()
        return self

    def switch_to_register_tab(self) -> "PlaywrightLoginPage":
        """Switch to Register tab."""
        self.register_tab.click()
        return self

    def switch_to_signin_tab(self) -> "PlaywrightLoginPage":
        """Switch to Sign In tab."""
        self.signin_tab.click()
        return self

    def get_error_message(self) -> str:
        """Wait for and get error message text."""
        self.error_alert.wait_for(state="visible", timeout=Config.DEFAULT_TIMEOUT * 1000)
        return self.error_alert.inner_text().strip()

    def is_error_visible(self, timeout: int = 5000) -> bool:
        """Check if error is visible within timeout ms."""
        try:
            self.error_alert.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
