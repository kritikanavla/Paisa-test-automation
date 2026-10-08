"""Playwright automation tests for Paisa Login page (https://paisa.ritadhi.com/login)."""
import pytest
from pages.playwright_login_page import PlaywrightLoginPage
from config.p_config import Config


@pytest.mark.playwright
class TestLoginPlaywright:
    """Fast, modern test suite for Paisa Login using Playwright."""

    def test_login_page_renders_successfully(self, playwright_page):
        """Verify URL and branding elements render with Playwright."""
        login_page = PlaywrightLoginPage(playwright_page).load()
        
        assert "paisa.ritadhi.com" in login_page.get_url()
        assert "Paisa" in login_page.get_title()
        assert login_page.welcome_heading.is_visible()
        assert login_page.sub_heading.is_visible()

    def test_login_inputs_and_button_visibility(self, playwright_page):
        """Verify input fields and submit button are visible and enabled."""
        login_page = PlaywrightLoginPage(playwright_page).load()
        
        assert login_page.email_input.is_visible()
        assert login_page.password_input.is_visible()
        assert login_page.submit_button.is_visible()
        assert login_page.submit_button.is_enabled()
        assert login_page.password_input.get_attribute("type") == "password"

    def test_invalid_login_shows_error_alert(self, playwright_page):
        """Verify invalid login triggers the red error banner."""
        login_page = PlaywrightLoginPage(playwright_page).load()
        
        login_page.login(Config.INVALID_EMAIL, Config.INVALID_PASSWORD)
        
        assert login_page.is_error_visible(timeout=10000), "Error message should become visible"
        error_text = login_page.get_error_message()
        assert "Invalid email or password" in error_text, f"Unexpected error message: {error_text}"

    @pytest.mark.parametrize("email,password", [
        ("user1@nonexistent123.com", "WrongPassword1!"),
        ("invalid.account@testcompany.org", "Pass_987654"),
    ])
    def test_parameterized_invalid_logins(self, playwright_page, email, password):
        """Verify multiple invalid login combinations trigger error banner."""
        login_page = PlaywrightLoginPage(playwright_page).load()
        login_page.login(email, password)
        
        assert login_page.is_error_visible(timeout=10000)
        assert "Invalid email or password" in login_page.get_error_message()

    def test_tab_switching(self, playwright_page):
        """Verify switching between Register and Sign In tabs."""
        login_page = PlaywrightLoginPage(playwright_page).load()
        
        login_page.switch_to_register_tab()
        assert login_page.email_input.is_visible()
        
        login_page.switch_to_signin_tab()
        assert login_page.email_input.is_visible()
