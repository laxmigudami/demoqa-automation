import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Configuration class"""

    # Project root
    BASE_DIR = Path(__file__).parent.parent

    # Paths
    REPORTS_PATH = BASE_DIR / "reports"
    LOGS_PATH = BASE_DIR / "logs"
    SCREENSHOTS_PATH = REPORTS_PATH / "screenshots"
    TEST_DATA_PATH = BASE_DIR / "test_data"

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 15))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 60))

    # URLs
    BASE_URL = os.getenv("BASE_URL", "https://demoqa.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://demoqa.com/BookStore/v1")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Screenshots
    TAKE_SCREENSHOTS = os.getenv("TAKE_SCREENSHOTS", "true").lower() == "true"
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

    # Retry
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", 2))


def get_config():
    """Get configuration instance"""
    return Config()
