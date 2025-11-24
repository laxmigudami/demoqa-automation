import re
from datetime import datetime
from pathlib import Path

from config.config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)
config = get_config()


class ScreenshotHandler:
    """
    Simplified screenshot handler for capturing and saving screenshots

    Features:
    - Single unified capture method
    - Automatic timestamp addition
    - Safe filename generation
    - Error handling with logging
    """

    def __init__(self, driver):
        """
        Initialize screenshot handler

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.screenshot_dir = config.SCREENSHOTS_PATH
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Screenshot directory: {self.screenshot_dir}")

    def take_screenshot(self, name, suffix=""):
        """
        Take and save screenshot with automatic timestamp

        Args:
            name: Base name for the screenshot
            suffix: Optional suffix to add (e.g., 'FAILED', 'ERROR')

        Returns:
            str: Path to saved screenshot or None if failed

        Example:
            take_screenshot("login_page")
            take_screenshot("checkout", suffix="FAILED")
        """
        try:
            # Build filename with optional suffix
            base_name = self._sanitize_filename(name)
            if suffix:
                base_name = f"{base_name}_{suffix}"

            # Add timestamp for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{base_name}_{timestamp}.png"
            filepath = self.screenshot_dir / filename

            # Capture screenshot
            if self.driver.save_screenshot(str(filepath)) and filepath.exists():
                file_size_kb = filepath.stat().st_size / 1024
                logger.info(f"Screenshot saved: {filename} ({file_size_kb:.1f} KB)")
                return str(filepath)

            logger.error(f"Failed to save screenshot: {filename}")
            return None

        except Exception as e:
            logger.error(f"Screenshot error for '{name}': {str(e)}")
            return None

    def _sanitize_filename(self, name):
        """
        Clean filename by removing invalid characters

        Args:
            name: Original filename

        Returns:
            str: Sanitized filename safe for Windows/Unix
        """
        # Replace invalid chars and spaces with underscore
        name = re.sub(r'[<>:"/\\|?*\s]+', "_", name)

        # Remove consecutive underscores
        name = re.sub(r"_+", "_", name)

        # Strip leading/trailing underscores
        name = name.strip("_")

        # Limit length (Windows 255 char limit)
        return name[:200] if len(name) > 200 else name
