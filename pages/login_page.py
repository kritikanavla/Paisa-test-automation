"""Page Object Model for the Paisa Login page."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from config.config import Config
from typing import Optional


class LoginPage(BasePage):
    """Encapsulates all locators, actions, and validations for the Paisa Login page."""

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SIGN_IN_TAB = (By.XPATH, "//button[contains(text(), 'Sign In') and not(@type='submit')]")
    REGISTER_TAB = (By.XPATH, "//button[contains(text(), 'Register')]")
    WELCOME_HEADING = (By.XPATH, "//*[contains(text(), 'Welcome to Paisa')]")
    SUB_HEADING = (By.XPATH, "//*[contains(text(), 'Intelligent Financial Analysis Platform')]")
    ERROR_ALERT = (By.XPATH, "//*[contains(@class, 'text-red-500') or contains(text(), 'Invalid email or password')]")

    def __init__(self, driver: WebDriver, timeout: int = Config.DEFAULT_TIMEOUT):
        super().__init__(driver, timeout)

    def load(self) -> "LoginPage":
        """Navigate directly to the Login page."""
        self.navigate_to(Config.LOGIN_URL)
        self.wait_for_page_ready()
        return self

    def wait_for_page_ready(self) -> bool:
        """Ensure critical login elements are rendered and visible."""
        return self.is_visible(self.EMAIL_INPUT) and self.is_visible(self.PASSWORD_INPUT)

    def enter_email(self, email: str) -> "LoginPage":
        """Type email address into the email input field."""
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Type password into the password input field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_sign_in_button(self) -> "LoginPage":
        """Click the Sign In submit button."""
        self.click(self.SUBMIT_BUTTON)
        return self

    def login(self, email: str, password: str) -> "LoginPage":
        """Convenience method to execute full login sequence."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_sign_in_button()
        return self

    def switch_to_register_tab(self) -> "LoginPage":
        """Click the Register tab switcher."""
        self.click(self.REGISTER_TAB)
        return self

    def switch_to_signin_tab(self) -> "LoginPage":
        """Click the Sign In tab switcher."""
        self.click(self.SIGN_IN_TAB)
        return self

    def get_error_message(self, timeout: int = 10) -> str:
        """Fetch error message text if displayed, otherwise returns empty string."""
        if self.is_visible(self.ERROR_ALERT, timeout=timeout):
            return self.get_text(self.ERROR_ALERT)
        return ""

    def is_error_displayed(self, timeout: int = 5) -> bool:
        """Check if an error banner/toast is currently visible."""
        return self.is_visible(self.ERROR_ALERT, timeout=timeout)

    def is_email_input_displayed(self) -> bool:
        """Check if email input field is visible."""
        return self.is_visible(self.EMAIL_INPUT)

    def is_password_input_displayed(self) -> bool:
        """Check if password input field is visible."""
        return self.is_visible(self.PASSWORD_INPUT)

    def is_submit_button_displayed(self) -> bool:
        """Check if submit button is visible."""
        return self.is_visible(self.SUBMIT_BUTTON)

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled."""
        element = self.find(self.SUBMIT_BUTTON)
        return element.is_enabled()

    def get_password_input_type(self) -> Optional[str]:
        """Verify password masking type attribute."""
        return self.get_attribute(self.PASSWORD_INPUT, "type")

    def get_email_input_placeholder(self) -> Optional[str]:
        """Get email placeholder attribute."""
        return self.get_attribute(self.EMAIL_INPUT, "placeholder")

    def get_password_input_placeholder(self) -> Optional[str]:
        """Get password placeholder attribute."""
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")

    def get_email_input_value(self) -> str:
        """Get current value typed inside email field."""
        return self.get_attribute(self.EMAIL_INPUT, "value") or ""

    def get_password_input_value(self) -> str:
        """Get current value typed inside password field."""
        return self.get_attribute(self.PASSWORD_INPUT, "value") or ""
