# Paisa Automation Testing Framework

Comprehensive Python test automation framework for testing login workflows, negative authentication cases, UI validation, and security behavior on **[https://paisa.ritadhi.com/login](https://paisa.ritadhi.com/login)**.

---

## 🌟 Framework Highlights
- **Page Object Model (POM)**: Complete separation of test logic, UI actions, and locator definitions for maintainability.
- **Dual Engine Support**:
  - **Playwright** (Lightning fast, built-in auto-waiting, parallel execution)
  - **Selenium WebDriver** (Standard enterprise WebDriver with dynamic explicit waits & `webdriver-manager`)
- **Pytest Integration**: Parameterized tests, custom markers (`selenium`, `playwright`), and HTML test reporting.
- **Auto Screenshot on Failure**: Failed test runs automatically capture full-page screenshots into `reports/screenshots/`.
- **Environment Driven**: Configurable via `.env` or system environment variables.

---

## 📁 Project Architecture

```
test project/
├── config/
│   └── config.py               # Central environment and test configuration
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Selenium BasePage with explicit waits & utilities
│   ├── login_page.py           # Selenium LoginPage Object Model
│   ├── playwright_base_page.py # Playwright BasePage
│   └── playwright_login_page.py# Playwright LoginPage Object Model
├── tests/
│   ├── __init__.py
│   ├── test_login_selenium.py  # Selenium Login test suite (positive & negative cases)
│   └── test_login_playwright.py# Playwright Login test suite
├── reports/                    # Generated test reports and failure screenshots
│   └── screenshots/
├── conftest.py                 # Pytest fixtures, browser management, failure hooks
├── pytest.ini                  # Pytest configuration & markers
├── requirements.txt            # Dependency list
├── .env.example                # Sample environment file
├── .env                        # Active environment configuration
└── README.md                   # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Recommended: `py -3.11`)
- Google Chrome browser installed

### 2. Install Dependencies
```bash
py -3.11 -m pip install -r requirements.txt
```

*(Optional for Playwright browser binaries):*
```bash
py -3.11 -m playwright install chromium
```

---

## 🧪 Running the Tests

### Run All Tests
```bash
py -3.11 -m pytest
```

### Run Playwright Tests
```bash
py -3.11 -m pytest -m playwright
# Or direct file:
py -3.11 -m pytest tests/test_login_playwright.py
```

### Run Selenium Tests
```bash
py -3.11 -m pytest -m selenium
# Or direct file:
py -3.11 -m pytest tests/test_login_selenium.py
```

### Run Specific Test Function
```bash
py -3.11 -m pytest tests/test_login_selenium.py -k "test_invalid_credentials_shows_error_message"
```

### Generate Self-Contained HTML Report
```bash
py -3.11 -m pytest --html=reports/report.html --self-contained-html
```

---

## ⚙️ Configuration & Headed Mode

You can control test settings directly inside `.env` or by passing environment variables:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://paisa.ritadhi.com` | Target web application URL |
| `HEADLESS` | `true` | Set to `false` to watch browser execution visually |
| `DEFAULT_TIMEOUT` | `15` | Default element wait timeout in seconds |
| `TEST_INVALID_EMAIL` | `invalid_user@example.com` | Test email for negative test scenarios |
| `TEST_INVALID_PASSWORD` | `WrongPassword123!` | Test password for negative scenarios |

### Example: Running with Browser UI Visible (Headed Mode)
In PowerShell:
```powershell
$env:HEADLESS="false"; py -3.11 -m pytest tests/test_login_playwright.py
```

---

## 🔍 Test Coverage
1. **Page Load & Branding**: Verifies page title, URL redirection, and header elements.
2. **Form Element Verification**: Confirms email input, password input, and Sign In button are visible, enabled, and have appropriate placeholders.
3. **Password Masking**: Validates that the password field has `type="password"`.
4. **Negative Authentication Scenarios**: Submits invalid credentials and asserts the display of the error message banner (`Invalid email or password.`).
5. **Parameterized Negative Cases**: Tests various malformed/non-existent account credentials.
6. **Tab Switching**: Tests switching between the **Sign In** and **Register** tabs.
7. **Input Retrieval**: Tests typing and value retrieval in form fields.
