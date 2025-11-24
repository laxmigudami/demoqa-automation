import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.locators import BookStorePageLocators
from utils.logger import Logger

logger = Logger(__name__).get_logger()


class BookStorePage(BasePage):
    """Book Store page class"""

    def __init__(self, driver):
        """Initialize book store page"""
        super().__init__(driver)
        self.locators = BookStorePageLocators()
        self.wait = WebDriverWait(driver, 15)

    def wait_for_book_table_to_load(self):
        """Wait for the book table to be visible and populated with data"""
        try:
            # Wait for table to be present
            self.wait.until(EC.presence_of_element_located(self.locators.BOOK_TABLE))
            logger.info("Book table is present")

            # Wait for at least one book row to be visible
            self.wait.until(EC.visibility_of_element_located(self.locators.BOOK_ROWS))
            logger.info("Book rows are visible")

            # Wait for the first book title to have text (ensuring data is loaded)
            self.wait.until(
                lambda driver: len(driver.find_elements(*self.locators.BOOK_TITLE_CELL)) > 0
                and driver.find_elements(*self.locators.BOOK_TITLE_CELL)[0].text.strip() != ""
            )
            logger.info("Book data is loaded")

            # Small buffer for any animations or dynamic loading
            time.sleep(1)

        except Exception as e:
            logger.error(f"Error waiting for book table to load: {e}")
            raise

    def search_book(self, book_title):
        """Search for book"""
        self.wait_for_book_table_to_load()

        # Find all matching search inputs and use the visible one
        search_inputs = self.find_elements(self.locators.SEARCH_INPUT)

        for search_input in search_inputs:
            if search_input.is_displayed() and search_input.is_enabled():
                search_input.clear()
                search_input.send_keys(book_title)
                time.sleep(1)  # Wait for search filter to apply
                logger.info(f"Searched for book: {book_title}")
                return

        raise Exception("No visible search input found")

    def get_all_books(self):
        """Get all books displayed on page"""
        try:
            self.wait_for_book_table_to_load()
        except Exception as e:
            # If wait times out, might be no results
            logger.info(f"Book table load wait timed out (possibly no results): {e}")
            return []

        book_rows = self.find_elements(self.locators.BOOK_ROWS)
        books = []

        for row in book_rows:
            try:
                title_element = row.find_element(*self.locators.BOOK_TITLE_CELL)
                title_text = title_element.text.strip()

                # Skip empty rows (pagination creates empty placeholder rows)
                if not title_text:
                    continue

                author_element = row.find_element(*self.locators.BOOK_AUTHOR_CELL)
                publisher_element = row.find_element(*self.locators.BOOK_PUBLISHER_CELL)

                # Get image element
                image_elements = row.find_elements(*self.locators.BOOK_IMAGE_CELL)
                image_src = image_elements[0].get_attribute("src") if image_elements else None

                book = {
                    "title": title_text,
                    "author": author_element.text.strip(),
                    "publisher": publisher_element.text.strip(),
                    "image": image_src,
                }
                books.append(book)

            except Exception as e:
                logger.warning(f"Error extracting book row: {e}")
                continue

        logger.info(f"Retrieved {len(books)} books from page")
        return books

    def get_book_by_title(self, title):
        """Get book by title"""
        try:
            self.wait_for_book_table_to_load()
            books = self.get_all_books()

            for book in books:
                if book["title"].lower().strip() == title.lower().strip():
                    logger.info(f"Found book: {title}")
                    return book

            logger.warning(f"Book not found: {title}")
            return None
        except Exception as e:
            # If wait_for_book_table_to_load times out, it might mean no results
            logger.info(f"No book table data found (possibly no search results): {e}")
            return None

    def get_total_books_count(self):
        """Get total number of books from pagination info or API"""
        try:
            # Since there's only 1 page, just count the books displayed
            books = self.get_all_books()
            total = len(books)
            logger.info(f"Total books count: {total}")
            return total

        except Exception as e:
            logger.error(f"Error getting total books count: {e}")
            return 0

    def is_book_image_displayed(self, book_title):
        """Check if the book image is displayed for a given book title"""
        self.wait_for_book_table_to_load()
        book_rows = self.find_elements(self.locators.BOOK_ROWS)

        for row in book_rows:
            try:
                title_element = row.find_element(*self.locators.BOOK_TITLE_CELL)

                if title_element.text.strip().lower() == book_title.strip().lower():
                    image_elements = row.find_elements(*self.locators.BOOK_IMAGE_CELL)

                    if image_elements:
                        image = image_elements[0]
                        is_displayed = image.is_displayed()
                        src = image.get_attribute("src")
                        has_valid_src = src and src.strip() != "" and not src.endswith("undefined")

                        if is_displayed and has_valid_src:
                            logger.info(f"Book image displayed for: {book_title} (src: {src})")
                            return True
                        else:
                            logger.warning(f"Book image element found but not properly displayed for: {book_title}")
                            return False
                    else:
                        logger.warning(f"Book image element NOT found for: {book_title}")
                        return False

            except Exception as e:
                logger.warning(f"Error checking book image for row: {e}")
                continue

        logger.warning(f"Book row not found for image check: {book_title}")
        return False

    # are_all_book_images_displayed method removed
