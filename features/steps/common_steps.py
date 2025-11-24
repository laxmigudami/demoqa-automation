from behave import given, then, when
from behave.runner import Context

from config.config import get_config
from pages.homepage import HomePage
from utils.logger import Logger

logger = Logger(__name__).get_logger()
config = get_config()


def _get_home_page(context: Context) -> HomePage:
    """Helper to initialize and return HomePage instance."""
    if not hasattr(context, "home_page"):
        context.home_page = HomePage(context.driver)
    return context.home_page


def _verify_url_contains(page: HomePage, expected_url_part: str, description: str = "URL") -> None:
    """Helper to verify URL contains expected part with proper error handling."""
    try:
        page.wait_for_url_contains(expected_url_part)
        current_url = page.get_current_url()
        assert (
            expected_url_part in current_url
        ), f"Expected {description} to contain '{expected_url_part}', but got: {current_url}"
    except Exception as e:
        logger.error(f"URL verification failed: {e}")
        raise


@given("the user has launched the DEMOQA application")
def step_launch_demoqa(context: Context) -> None:
    """Launch the DEMOQA application in the browser."""
    try:
        home_page = _get_home_page(context)
        home_page.navigate_to(config.BASE_URL)
        current_url = home_page.get_current_url()
        assert "demoqa.com" in current_url, f"Failed to launch DEMOQA application. Current URL: {current_url}"
    except Exception as e:
        logger.error(f"Failed to launch DEMOQA application: {e}")
        raise


@when('the user clicks on "Elements" card')
@given('the user clicks on "Elements" card')
def step_click_elements_card(context: Context) -> None:
    """Click on the Elements card on the homepage."""
    _get_home_page(context).click_elements_card()


@then('the user should be navigated to a URL containing "demoqa.com/elements"')
def step_verify_elements_url(context: Context) -> None:
    """Verify navigation to the Elements page."""
    _verify_url_contains(_get_home_page(context), "demoqa.com/elements", "Elements page URL")


@then('the menu list for "Elements" should be expanded')
def step_elements_menu_expanded(context: Context) -> None:
    """Verify that the Elements menu is expanded."""
    try:
        assert _get_home_page(context).is_elements_menu_expanded(), "Elements menu is not expanded as expected"
    except Exception as e:
        logger.error(f"Elements menu expansion verification failed: {e}")
        raise


@then('the menu list items for "Elements" should be')
def step_elements_menu_items(context: Context) -> None:
    """Verify that the Elements menu contains the expected items."""
    try:
        expected_items = [row[0] for row in context.table]
        actual_items = _get_home_page(context).get_elements_menu_items()

        expected_set = set(expected_items)
        actual_set = set(actual_items)

        assert (
            expected_set == actual_set
        ), f"Elements menu items mismatch - Expected: {sorted(expected_items)}, Actual: {sorted(actual_items)}"
    except Exception as e:
        logger.error(f"Menu items verification failed: {e}")
        raise
