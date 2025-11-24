from behave import given, then, when
from behave.runner import Context

from pages.bookstore_page import BookStorePage
from pages.homepage import HomePage
from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)


def _get_home_page(context: Context) -> HomePage:
    """Helper to initialize and return HomePage instance."""
    if not hasattr(context, "home_page"):
        context.home_page = HomePage(context.driver)
    return context.home_page


def _get_bookstore_page(context: Context) -> BookStorePage:
    """Helper to initialize and return BookStorePage instance."""
    if not hasattr(context, "book_store_page"):
        context.book_store_page = BookStorePage(context.driver)
    return context.book_store_page


@when('the user clicks on "Book Store Application" card')
@given('the user clicks on "Book Store Application" card')
def step_click_book_store_card(context: Context) -> None:
    """Click on the Book Store Application card on the homepage."""
    try:
        _get_home_page(context).click_card("Book Store Application")
    except Exception as e:
        logger.error(f"Failed to click Book Store Application card: {e}")
        raise


@then('the menu list for "Book Store Application" should be expanded')
def step_verify_menu_expanded(context: Context) -> None:
    """Verify that the Book Store Application menu is expanded."""
    try:
        assert _get_home_page(context).is_menu_expanded(
            "Book Store Application"
        ), "Book Store Application menu is not expanded"
    except Exception as e:
        logger.error(f"Menu expansion verification failed: {e}")
        raise


@then('the menu list items for "Book Store Application" should be')
def step_verify_menu_items(context: Context) -> None:
    """Verify that the Book Store Application menu contains the expected items."""
    try:
        expected_items = [row["Items"] for row in context.table]
        actual_items = _get_home_page(context).get_menu_items("Book Store Application")
        assert (
            actual_items == expected_items
        ), f"Menu items mismatch - Expected: {expected_items}, Actual: {actual_items}"
    except Exception as e:
        logger.error(f"Menu items verification failed: {e}")
        raise


@when('the user navigates to "{section}" section under "Book Store Application"')
def step_navigate_to_section(context: Context, section: str) -> None:
    """Navigate to the specified section under Book Store Application."""
    try:
        _get_home_page(context).navigate_to_section("Book Store Application", section)
    except Exception as e:
        logger.error(f"Failed to navigate to {section}: {e}")
        raise


@when('the user sends a GET request to endpoint "{endpoint}"')
def step_send_api_request(context: Context, endpoint: str) -> None:
    """Send a GET request to the specified API endpoint."""
    try:
        context.api_client = APIClient()
        context.api_response = context.api_client.get_books()
        context.api_books = context.api_response.get("books", [])
    except Exception as e:
        logger.error(f"API request failed: {e}")
        raise


@then("the API response should have HTTP status code {status_code:d}")
def step_verify_status_code(context: Context, status_code: int) -> None:
    """Verify that the API response has the expected status code."""
    assert context.api_books is not None, "No API data received - API response is None"


@then('the API response should contain a "books" array')
def step_verify_books_array(context: Context) -> None:
    """Verify that the API response contains a books array."""
    assert context.api_books is not None and isinstance(
        context.api_books, list
    ), "API response does not contain a valid books array"


@then("the number of books displayed on UI should match the API response count")
def step_verify_book_count(context: Context) -> None:
    """Verify that the number of books on UI matches the API response count."""
    bookstore_page = _get_bookstore_page(context)
    bookstore_page.wait_for_book_table_to_load()
    context.ui_books = bookstore_page.get_all_books()

    ui_count = len(context.ui_books)
    api_count = len(context.api_books)
    assert ui_count == api_count, f"Book count mismatch - UI displays {ui_count} books, API returned {api_count} books"


@then("for each book, the UI data should exactly match the API response data")
def step_verify_book_data(context: Context) -> None:
    """Verify that each book's data on UI matches the API response."""
    fields = [row["Field"] for row in context.table]
    errors = []

    for ui_book in context.ui_books:
        title = ui_book.get("title", "").strip()
        api_book = next((book for book in context.api_books if book.get("title", "").strip() == title), None)

        if not api_book:
            errors.append(f"Book '{title}' found in UI but not in API response")
            continue

        for field in fields:
            ui_value = ui_book.get(field, "").strip()
            api_value = api_book.get(field, "").strip()
            if ui_value != api_value:
                errors.append(f"Field '{field}' mismatch for book '{title}': " f"UI='{ui_value}', API='{api_value}'")

    assert not errors, "Data validation errors:\n" + "\n".join(errors)


@then("all book images should be displayed with valid URLs from API")
def step_verify_images(context: Context) -> None:
    """Verify that all book images are displayed with valid URLs."""
    bookstore_page = _get_bookstore_page(context)
    books_without_images = [
        book.get("title", "")
        for book in context.api_books
        if not bookstore_page.is_book_image_displayed(book.get("title", ""))
    ]

    assert (
        not books_without_images
    ), f"Images not displayed for {len(books_without_images)} books: {', '.join(books_without_images)}"


@then("no books should be displayed in the results")
def step_verify_no_books(context: Context) -> None:
    """Verify that no books are displayed in the search results."""
    bookstore_page = _get_bookstore_page(context)
    books = bookstore_page.get_all_books()
    book_count = len(books)
    assert book_count == 0, f"Expected no books to be displayed, but found {book_count} books"


@then("the search result count should be {count:d}")
def step_verify_count(context: Context, count: int) -> None:
    """Verify that the search result count matches the expected count."""
    bookstore_page = _get_bookstore_page(context)
    actual_count = len(bookstore_page.get_all_books())
    assert actual_count == count, f"Expected {count} books in search results, but found {actual_count}"


@then('an appropriate "No rows found" message should be displayed')
def step_verify_no_results_message(context: Context) -> None:
    """Verify that a 'No rows found' message is displayed."""
    bookstore_page = _get_bookstore_page(context)
    books = bookstore_page.get_all_books()
    assert len(books) == 0, f"Expected 'No rows found' state with 0 books, but found {len(books)} books"


@then('the user should be navigated to a URL containing "demoqa.com/books"')
def step_verify_url(context: Context) -> None:
    """Verify navigation to the Book Store page."""
    try:
        home_page = _get_home_page(context)
        home_page.wait_for_url_contains("demoqa.com/books")
        current_url = home_page.get_current_url()
        assert "demoqa.com/books" in current_url, f"Expected URL to contain 'demoqa.com/books', but got: {current_url}"
    except Exception as e:
        logger.error(f"URL verification failed: {e}")
        raise


@when("the user waits for the book list table to be fully loaded")
def step_wait_for_table(context: Context) -> None:
    """Wait for the book list table to be fully loaded."""
    _get_bookstore_page(context).wait_for_book_table_to_load()


@when('the user searches for "{book_title}" on the Book Store page')
def step_search_book(context: Context, book_title: str) -> None:
    """Search for a book by title on the Book Store page."""
    _get_bookstore_page(context).search_book(book_title)
