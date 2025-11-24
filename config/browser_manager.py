from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import get_config
from utils.logger import Logger

logger = Logger(__name__).get_logger()
config = get_config()


class BrowserManager:
    """Browser setup and teardown"""

    @staticmethod
    def setup_browser():
        """
        Initialize WebDriver

        Returns:
            WebDriver instance
        """
        browser = config.BROWSER.lower()
        logger.info(f"Setting up {browser} browser...")

        if browser == "chrome":
            options = ChromeOptions()
            if config.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            # Maximize the window after starting Chrome
            driver.maximize_window()
        elif browser == "firefox":
            options = FirefoxOptions()

            if config.HEADLESS:
                options.add_argument("--headless")

            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # Set timeouts
        driver.implicitly_wait(config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

        logger.info(f"WebDriver configured - Browser: {browser}, Headless: {config.HEADLESS}")

        return driver

    @staticmethod
    def teardown_browser(driver):
        """Close WebDriver with graceful cleanup"""
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver closed")
            except Exception as e:
                # Suppress cleanup exceptions during shutdown
                logger.debug(f"Driver cleanup exception (can be ignored): {e}")
                try:
                    # Force close if quit failed
                    driver.close()
                except Exception:
                    pass
