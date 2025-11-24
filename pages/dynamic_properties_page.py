import time

from pages.base_page import BasePage
from pages.locators import DynamicPropertiesPageLocators
from utils.logger import Logger

logger = Logger(__name__).get_logger()


class DynamicPropertiesPage(BasePage):
    """Dynamic Properties page class."""

    def __init__(self, driver):
        """Initialize dynamic properties page."""
        super().__init__(driver)
        self.locators = DynamicPropertiesPageLocators()

    def is_visible_after_5_seconds_button_visible(self):
        """Check if 'Visible After 5 Seconds' button is visible."""
        return self.is_element_visible_now(self.locators.VISIBLE_AFTER_5_SECONDS_BUTTON)

    def wait_for_visible_after_5_seconds_button(self, timeout=10):
        """Wait for 'Visible After 5 Seconds' button to be visible.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            bool: True if button becomes visible, False otherwise
        """
        try:
            self.wait_for_element_visible(self.locators.VISIBLE_AFTER_5_SECONDS_BUTTON, timeout=timeout)
            logger.info("'Visible After 5 Seconds' button is now visible")
            return True
        except Exception as e:
            logger.error(f"Error waiting for button visibility: {e}")
            return False

    def get_color_change_button_color(self):
        """Get current text color of 'Color Change' button.

        Returns:
            str: Color value or None if error occurs
        """
        try:
            color = self.get_element_css_property(self.locators.COLOR_CHANGE_BUTTON, "color")
            logger.info(f"Color Change button color: {color}")
            return color
        except Exception as e:
            logger.error(f"Error getting button color: {e}")
            return None

    def get_color_change_button_background_color(self):
        """Get background color of 'Color Change' button.

        Returns:
            str: Background color value or None if error occurs
        """
        try:
            color = self.get_element_css_property(self.locators.COLOR_CHANGE_BUTTON, "background-color")
            logger.info(f"Color Change button background color: {color}")
            return color
        except Exception as e:
            logger.error(f"Error getting button background color: {e}")
            return None

    def wait_for_color_change(self, timeout=10, property_name="color"):
        """Wait for button color property to change.

        Args:
            timeout: Maximum time to wait in seconds
            property_name: CSS property to check ('color' or 'background-color')

        Returns:
            bool: True if color changed, False otherwise
        """
        try:
            if property_name == "color":
                initial_color = self.get_color_change_button_color()
            elif property_name == "background-color":
                initial_color = self.get_color_change_button_background_color()
            else:
                logger.error(f"Unsupported property name: {property_name}")
                return False

            if initial_color is None:
                logger.error("Failed to get initial color")
                return False

            logger.info(f"Waiting for {property_name} to change from: {initial_color}")

            start_time = time.time()
            check_interval = 0.5

            while time.time() - start_time < timeout:
                current_color = (
                    self.get_color_change_button_color()
                    if property_name == "color"
                    else self.get_color_change_button_background_color()
                )

                if current_color and current_color != initial_color:
                    elapsed = round(time.time() - start_time, 2)
                    logger.info(f"{property_name} changed after {elapsed}s: {initial_color} -> {current_color}")
                    return True

                time.sleep(check_interval)

            elapsed = round(time.time() - start_time, 2)
            logger.warning(f"{property_name} did not change within {elapsed}s (timeout: {timeout}s)")
            return False

        except Exception as e:
            logger.error(f"Error waiting for color change: {e}")
            return False
