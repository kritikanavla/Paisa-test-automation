"""Configuration settings for Paisa UI automation tests."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://paisa.ritadhi.com")
    LOGIN_URL = f"{BASE_URL}/login"
    
    # Timeouts (seconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "15"))
    SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", "5"))
    
    # Test credentials (default or from .env)
    VALID_EMAIL = os.getenv("TEST_VALID_EMAIL", "user@example.com")
    VALID_PASSWORD = os.getenv("TEST_VALID_PASSWORD", "SecretPassword123!")
    
    INVALID_EMAIL = os.getenv("TEST_INVALID_EMAIL", "invalid_qa_user@example.com")
    INVALID_PASSWORD = os.getenv("TEST_INVALID_PASSWORD", "WrongPassword999!")
    
    # Browser configuration
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
