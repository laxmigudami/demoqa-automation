from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.locators import ElementsMenuLocators, HomePageLocators
from utils.logger import Logger

logger = Logger(__name__).get_logger()


class HomePage(BasePage):
    """Home page class"""

    def __init__(self, driver):
        """Initialize home page"""
        super().__init__(driver)
        self.locators = HomePageLocators()
        self.elements_menu_locators = ElementsMenuLocators()

    def click_forms_card(self):
        """Click on Forms card"""
        try:
            self.wait_for_element_clickable(self.locators.FORMS_CARD, timeout=10)
            self.click_element(self.locators.FORMS_CARD)
            logger.info("Clicked on Forms card")
        except Exception as e:
            logger.error(f"Failed to click Forms card: {e}")
            raise

    def click_book_store_card(self):
        """Click on Book Store Application card"""
        try:
            self.wait_for_element_clickable(self.locators.BOOK_STORE_APPLICATION_CARD, timeout=10)
            self.click_element(self.locators.BOOK_STORE_APPLICATION_CARD)
            logger.info("Clicked on Book Store Application card")
        except Exception as e:
            logger.error(f"Failed to click Book Store Application card: {e}")
            raise

    def click_elements_card(self):
        """Click on Elements card"""
        try:
            self.wait_for_element_clickable(self.locators.ELEMENTS_CARD, timeout=10)
            self.click_element(self.locators.ELEMENTS_CARD)
            logger.info("Clicked on Elements card")
        except Exception as e:
            logger.error(f"Failed to click Elements card: {e}")
            raise

    def is_elements_menu_expanded(self):
        """Check if Elements menu is expanded"""
        try:
            menu_items = self.find_elements((By.XPATH, "//span[contains(text(), 'Text Box')]"))
            return len(menu_items) > 0
        except Exception as e:
            logger.error(f"Error checking menu expansion: {e}")
            return False

    def get_elements_menu_items(self):
        """Get all Elements menu items"""
        try:
            items = []
            # Match the test expectation for 'Broken Links - Images'
            item_names = [
                "Text Box",
                "Check Box",
                "Radio Button",
                "Web Tables",
                "Buttons",
                "Links",
                "Broken Links - Images",
                "Upload and Download",
                "Dynamic Properties",
            ]
            # Try both 'Broken Links' and 'Broken Links - Images' for robustness
            for item_name in item_names:
                locator = self.elements_menu_locators.get_menu_item(
                    "Broken Links" if item_name == "Broken Links - Images" else item_name
                )
                if self.is_element_present(locator):
                    items.append(item_name)
            logger.info(f"Found Elements menu items: {items}")
            return items
        except Exception as e:
            logger.error(f"Error getting menu items: {e}")
            return []

    def navigate_to_menu_item(self, item_name):
        """Navigate to menu item"""
        try:
            locator = self.elements_menu_locators.get_menu_item(item_name)
            self.wait_for_element_visible(locator, timeout=10)
            self.click_element(locator)
            logger.info(f"Navigated to: {item_name}")
        except Exception as e:
            logger.error(f"Error navigating to menu item '{item_name}': {e}")
            raise

    def click_card(self, card_name):
        """Click on a card by name (generic method)"""
        try:
            card_locator = (By.XPATH, f"//h5[contains(text(), '{card_name}')]")
            self.wait_for_element_visible(card_locator, timeout=10)
            self.click_element(card_locator)
            logger.info(f"Clicked on {card_name} card")
        except Exception as e:
            logger.error(f"Error clicking on {card_name} card: {e}")
            raise

    def is_menu_expanded(self, section_name):
        """Check if menu for a section is expanded"""
        try:
            # Check if any menu items are visible after clicking the card
            # For Book Store Application, we expect Login, Book Store, Profile, Book Store API
            menu_items = self.get_menu_items(section_name)
            is_expanded = len(menu_items) > 0
            logger.info(f"{section_name} menu expanded: {is_expanded}")
            return is_expanded
        except Exception as e:
            logger.error(f"Error checking if {section_name} menu is expanded: {e}")
            return False

    def get_menu_items(self, section_name):
        """Get menu items for a specific section"""
        try:
            items = []

            if section_name == "Elements":
                # Elements menu items
                item_names = [
                    "Text Box",
                    "Check Box",
                    "Radio Button",
                    "Web Tables",
                    "Buttons",
                    "Links",
                    "Broken Links - Images",
                    "Upload and Download",
                    "Dynamic Properties",
                ]
                for item_name in item_names:
                    locator = self.elements_menu_locators.get_menu_item(
                        "Broken Links" if item_name == "Broken Links - Images" else item_name
                    )
                    if self.is_element_present(locator):
                        items.append(item_name)

            elif section_name == "Book Store Application":
                # Book Store Application menu items
                item_names = ["Login", "Book Store", "Profile", "Book Store API"]
                for item_name in item_names:
                    locator = (By.XPATH, f"//span[contains(text(), '{item_name}')]")
                    if self.is_element_present(locator):
                        items.append(item_name)

            elif section_name == "Forms":
                # Forms menu items
                item_names = ["Practice Form"]
                for item_name in item_names:
                    locator = (By.XPATH, f"//span[contains(text(), '{item_name}')]")
                    if self.is_element_present(locator):
                        items.append(item_name)

            logger.info(f"Found {section_name} menu items: {items}")
            return items

        except Exception as e:
            logger.error(f"Error getting menu items for {section_name}: {e}")
            return []

    def navigate_to_section(self, category, section):
        """Navigate to a section under a category"""
        try:
            locator = (By.XPATH, f"//span[contains(text(), '{section}')]")
            self.wait_for_element_visible(locator, timeout=10)
            self.click_element(locator)
            logger.info(f"Navigated to: {section}")
        except Exception as e:
            logger.error(f"Error navigating to section '{section}' under '{category}': {e}")
            raise
