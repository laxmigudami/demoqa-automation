from selenium.webdriver.common.by import By


class HomePageLocators:
    """Home page locators"""

    FORMS_CARD = (By.XPATH, "//h5[contains(text(), 'Forms')]")
    BOOK_STORE_APPLICATION_CARD = (By.XPATH, "//h5[contains(text(), 'Book Store Application')]")
    ELEMENTS_CARD = (By.XPATH, "//h5[contains(text(), 'Elements')]")


class ElementsMenuLocators:
    """Elements menu locators"""

    @staticmethod
    def get_menu_item(item_name):
        """Get menu item by name"""
        return (By.XPATH, f"//span[contains(text(), '{item_name}')]")


class FormsPageLocators:
    """Forms page locators"""

    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='First Name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='Last Name']")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='name@example.com']")
    MOBILE_INPUT = (By.XPATH, "//input[@placeholder='Mobile Number']")
    GENDER_FEMALE_RADIO = (By.XPATH, "//input[@value='Female']")
    GENDER_MALE_RADIO = (By.XPATH, "//input[@value='Male']")
    GENDER_FEMALE_LABEL = (By.XPATH, "//label[@for='gender-radio-2']")
    GENDER_MALE_LABEL = (By.XPATH, "//label[@for='gender-radio-1']")
    DATE_OF_BIRTH_INPUT = (By.XPATH, "//input[@id='dateOfBirthInput']")
    CURRENT_ADDRESS_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Current Address']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Submit')]")
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class, 'modal-content')]")
    SUCCESS_MODAL_TITLE = (By.XPATH, "//*[contains(text(), 'Thanks for submitting the form')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(text(), 'Close')]")
    MODAL_TABLE_ROWS = (By.XPATH, "//div[contains(@class, 'modal-content')]//td")


class BookStorePageLocators:
    """Locators for Book Store page"""

    # Table elements
    BOOK_TABLE = (By.CSS_SELECTOR, ".rt-table")
    BOOK_ROWS = (By.CSS_SELECTOR, ".rt-tr-group")

    # Book details cells
    BOOK_IMAGE_CELL = (By.XPATH, ".//div[contains(@class, 'rt-td')][1]//img")
    BOOK_TITLE_CELL = (By.XPATH, ".//div[contains(@class, 'rt-td')][2]")
    BOOK_AUTHOR_CELL = (By.CSS_SELECTOR, ".rt-td:nth-child(3)")
    BOOK_PUBLISHER_CELL = (By.CSS_SELECTOR, ".rt-td:nth-child(4)")

    # Search
    SEARCH_INPUT = (By.CSS_SELECTOR, "div.mb-3.input-group input#searchBox[placeholder='Type to search']")


class CheckBoxPageLocators:
    """Locators for Checkbox page with optimized XPath expressions"""

    # Expand/Collapse All buttons - using title attribute for precise selection
    EXPAND_ALL_BUTTON = (By.XPATH, "//button[@title='Expand all']")
    COLLAPSE_ALL_BUTTON = (By.XPATH, "//button[@title='Collapse all']")

    # Tree node toggle icons (for individual nodes, not the main buttons)
    COLLAPSE_ICONS = (By.XPATH, "//button[contains(@class, 'rct-collapse')]")
    EXPAND_ICONS = (By.XPATH, "//button[contains(@class, 'rct-expand')]")

    # Tree nodes - all visible node titles
    TREE_NODES = (By.XPATH, "//span[@class='rct-title']")

    # Result display area
    RESULT_TEXT = (By.ID, "result")

    @staticmethod
    def get_node_by_name(node_name):
        """Get node element by its text name"""
        return (By.XPATH, f"//span[@class='rct-title' and text()='{node_name}']")

    @staticmethod
    def get_node_parent(node_name):
        """Get parent li element of a node (contains entire node structure)"""
        return (By.XPATH, f"//span[@class='rct-title' and text()='{node_name}']/ancestor::li[1]")

    @staticmethod
    def get_checkbox_for_node(node_name):
        """Get checkbox span element for a node"""
        return (
            By.XPATH,
            f"//span[@class='rct-title' and text()='{node_name}']/"
            f"preceding-sibling::span[contains(@class, 'rct-checkbox')]",
        )

    @staticmethod
    def get_node_input(node_name):
        """Get the actual checkbox input element for a node"""
        return (
            By.XPATH,
            f"//span[@class='rct-title' and text()='{node_name}']/ancestor::label//input[@type='checkbox']",
        )


class DynamicPropertiesPageLocators:
    """Dynamic Properties page locators"""

    # Buttons
    VISIBLE_AFTER_5_SECONDS_BUTTON = (By.XPATH, "//button[contains(text(), 'Visible After 5 Seconds')]")
    COLOR_CHANGE_BUTTON = (By.XPATH, "//button[contains(text(), 'Color Change')]")
