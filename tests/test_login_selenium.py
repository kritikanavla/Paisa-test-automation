"""Selenium automation tests for Paisa Login page (https://paisa.ritadhi.com/login)."""
import pytest
from pages.login_page import LoginPage
from config.p_config import Config


@pytest.mark.selenium
class TestLoginSelenium:
    """Test suite verifying Login page functionality, security, validation, and error states."""

    def test_login_page_loads_successfully(self, driver):
        """Verify the login page URL, page title, and key branding elements load."""
        login_page = LoginPage(driver).load()
        
        assert "paisa.ritadhi.com" in login_page.get_current_url(), "URL should contain paisa.ritadhi.com"
        assert "Paisa" in login_page.get_title(), f"Page title '{login_page.get_title()}' should contain 'Paisa'"
        assert login_page.is_visible(LoginPage.WELCOME_HEADING), "Welcome heading should be visible"
        assert login_page.is_visible(LoginPage.SUB_HEADING), "Sub-heading should be visible"

    def test_login_form_elements_present_and_enabled(self, driver):
        """Verify email input, password input, and Sign In submit button are visible and interactive."""
        login_page = LoginPage(driver).load()
        
        assert login_page.is_email_input_displayed(), "Email input field should be visible"
        assert login_page.is_password_input_displayed(), "Password input field should be visible"
        assert login_page.is_submit_button_displayed(), "Sign In button should be visible"
        assert login_page.is_submit_button_enabled(), "Sign In button should be enabled"
        
        # Check input placeholders
        assert "email" in login_page.get_email_input_placeholder().lower(), "Email input placeholder should indicate email"
        assert "password" in login_page.get_password_input_placeholder().lower(), "Password input placeholder should indicate password"

    def test_password_field_is_masked(self, driver):
        """Verify the password input masks user input with type='password'."""
        login_page = LoginPage(driver).load()
        input_type = login_page.get_password_input_type()
        
        assert input_type == "password", f"Password input type must be 'password' to mask input, got: {input_type}"

    def test_invalid_credentials_shows_error_message(self, driver):
        """Verify that submitting invalid credentials displays 'Invalid email or password.' error alert."""
        login_page = LoginPage(driver).load()
        
        login_page.login(Config.INVALID_EMAIL, Config.INVALID_PASSWORD)
        
        assert login_page.is_error_displayed(timeout=10), "Error banner should be displayed on invalid credentials"
        error_msg = login_page.get_error_message()
        assert "Invalid email or password" in error_msg, f"Expected 'Invalid email or password' in error, got: '{error_msg}'"

    @pytest.mark.parametrize("email,password", [
        ("nonexistent_user_987654@test.com", "Password@123456"),
        ("admin@randomdomainnotexist.io", "AdminWrongPass123"),
        ("test.qa.automation@gmail.com", "Wrong1234!"),
    ])
    def test_multiple_invalid_credentials_negative_cases(self, driver, email, password):
        """Parameterized test checking error display across various invalid credentials."""
        login_page = LoginPage(driver).load()
        
        login_page.login(email, password)
        
        assert login_page.is_error_displayed(timeout=10), f"Error banner should be displayed for {email}"
        assert "Invalid email or password" in login_page.get_error_message()

    def test_switch_between_signin_and_register_tabs(self, driver):
        """Verify user can switch between 'Sign In' and 'Register' tabs smoothly."""
        login_page = LoginPage(driver).load()
        
        # Switch to Register tab
        login_page.switch_to_register_tab()
        assert login_page.is_email_input_displayed(), "Email input should be present on Register tab"
        assert login_page.is_password_input_displayed(), "Password input should be present on Register tab"
        
        # Switch back to Sign In tab
        login_page.switch_to_signin_tab()
        assert login_page.is_email_input_displayed(), "Email input should be present on Sign In tab"
        assert login_page.is_password_input_displayed(), "Password input should be present on Sign In tab"

    def test_input_text_retrieval(self, driver):
        """Verify entered text in fields matches typed values."""
        login_page = LoginPage(driver).load()
        
        test_email = "automation_tester@domain.com"
        test_pwd = "MySecretTestingPass#2026"
        
        login_page.enter_email(test_email)
        login_page.enter_password(test_pwd)
        
        assert login_page.get_email_input_value() == test_email, "Email field value should match typed string"
        assert login_page.get_password_input_value() == test_pwd, "Password field value should match typed string"
