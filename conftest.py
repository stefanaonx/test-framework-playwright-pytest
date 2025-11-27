pytest_bdd_features_path = "kiwi_tests/features"

import pytest
from playwright.sync_api import Page, BrowserContext # Import Page and BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "en-US", # Recommended for consistent language
        "geolocation": {"latitude": 51.5074, "longitude": 0.1278}, # Example: London, UK
        "permissions": ["geolocation"],
        "extra_http_headers": {"Accept-Language": "en-US,en;q=0.9"},
    }

@pytest.fixture(autouse=True)
def handle_privacy_popup_automatically(page: Page):
    # This script runs before any of the page's JavaScript - first line of defense
    page.add_init_script('''
        Object.defineProperty(navigator, 'cookieEnabled', { get: () => true });
        localStorage.setItem('cookie_consent', 'true');
        document.cookie = '_kwc_agreed=true; domain=.kiwi.com; path=/; max-age=31536000';
        document.cookie = '_kwc_settings=%7B%22marketing%22%3Atrue%2C%22analytics%22%3Atrue%7D; domain=.kiwi.com; path=/; max-age=31536000';
    ''')
