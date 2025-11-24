from typing import List, Optional

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import get_config
from utils.logger import Logger
from utils.screenshot_handler import ScreenshotHandler

config = get_config()
logger = Logger(__name__).get_logger()


class BasePage:
    """Base page class with common methods for page objects."""

    def __init__(self, driver: WebDriver) -> None:
        """Initialize the base page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
        self.actions = ActionChains(driver)
        self.screenshot_handler = ScreenshotHandler(driver)

    def is_element_visible_now(self, locator: tuple) -> bool:
        """Check if element is visible immediately without wait."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def navigate_to(self, url: str) -> None:
        """Navigate to URL with retry logic."""
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                self.driver.get(url)
                logger.info(f"Navigated to: {url}")
                # Wait for page to be ready
                self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                return
            except Exception:
                if attempt < max_retries:
                    logger.warning(f"Navigation failed (attempt {attempt + 1}/{max_retries + 1}), retrying...")
                    # Brief wait before retry using explicit wait
                    try:
                        WebDriverWait(self.driver, 2).until(lambda d: False)
                    except Exception:
                        pass
                else:
                    logger.error(f"Navigation failed after {max_retries + 1} attempts")
                    raise

    def get_current_url(self) -> str:
        """Get the current URL."""
        return self.driver.current_url

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()
        logger.info("Page refreshed")

    def find_element(self, locator: tuple, log_error: bool = True) -> WebElement:
        """Find element with explicit wait."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except Exception as e:
            if log_error:
                logger.error(f"Element not found {locator}: {e}")
            raise

    def find_elements(self, locator: tuple) -> List[WebElement]:
        """Find multiple elements."""
        try:
            return self.driver.find_elements(*locator)
        except Exception as e:
            logger.error(f"Error finding elements {locator}: {e}")
            return []

    def click_element(self, locator: tuple) -> None:
        """Click element with overlay handling and retry logic."""
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                # Remove ads and overlays
                self.driver.execute_script(
                    "['fixedban', 'adplus-anchor'].forEach(id => { "
                    "const el = document.getElementById(id); if (el) el.remove(); });"
                )

                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                # Wait for element to be stable after scroll
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(locator))

                try:
                    element.click()
                    return  # Success
                except Exception:
                    logger.warning("Regular click failed, trying JavaScript click")
                    self.driver.execute_script("arguments[0].click();", element)
                    return  # Success

            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"Click attempt {attempt + 1} failed, retrying... {e}")
                    # Wait before retry using explicit wait
                    try:
                        WebDriverWait(self.driver, 1).until(lambda d: False)
                    except Exception:
                        pass
                else:
                    logger.error(f"Click failed after {max_retries + 1} attempts {locator}: {e}")
                    raise

    def enter_text(self, locator: tuple, text: str) -> None:
        """Enter text in element."""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logger.error(f"Text entry failed {locator}: {e}")
            raise

    def get_text(self, locator: tuple) -> Optional[str]:
        """Get text from element."""
        try:
            return self.find_element(locator, log_error=False).text
        except Exception as e:
            logger.error(f"Get text failed {locator}: {e}")
            return None

    def is_element_visible(self, locator: tuple) -> bool:
        """Check if element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present in DOM."""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def is_element_enabled(self, locator: tuple) -> bool:
        """Check if element is enabled."""
        try:
            return self.find_element(locator).is_enabled()
        except Exception:
            return False

    def wait_for_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Wait for element to be visible."""
        try:
            WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT).until(EC.visibility_of_element_located(locator))
        except Exception:
            logger.error(f"Timeout: element not visible {locator}")
            raise

    def wait_for_element_clickable(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Wait for element to be clickable."""
        try:
            WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT).until(EC.element_to_be_clickable(locator))
        except Exception:
            logger.error(f"Timeout: element not clickable {locator}")
            raise

    def wait_for_url_contains(self, url_part: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to contain text."""
        try:
            WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT).until(EC.url_contains(url_part))
        except Exception:
            logger.error(f"Timeout: URL does not contain {url_part}")
            raise

    def wait_for_element_invisible(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Wait for element to be invisible."""
        try:
            WebDriverWait(self.driver, timeout or config.EXPLICIT_WAIT).until(
                EC.invisibility_of_element_located(locator)
            )
        except Exception:
            logger.error(f"Timeout: element still visible {locator}")
            raise

    def scroll_to_element(self, locator: tuple) -> None:
        """Scroll to element."""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # Wait for scroll to complete by checking element is in viewport
            self.wait.until(
                lambda d: d.execute_script(
                    "return arguments[0].getBoundingClientRect().top >= 0 && "
                    "arguments[0].getBoundingClientRect().bottom <= window.innerHeight",
                    element,
                )
            )
        except Exception as e:
            logger.error(f"Scroll failed {locator}: {e}")
            raise

    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript."""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"Script execution failed: {e}")
            raise

    def get_element_css_property(self, locator: tuple, property_name: str) -> Optional[str]:
        """Get CSS property value."""
        try:
            element = self.find_element(locator)
            return element.value_of_css_property(property_name)
        except Exception as e:
            logger.error(f"Get CSS property failed: {e}")
            return None

    def take_screenshot(self, name: str) -> None:
        """Take screenshot."""
        self.screenshot_handler.take_screenshot(name)
