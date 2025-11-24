import time

from behave import given, then, when

from pages.dynamic_properties_page import DynamicPropertiesPage
from utils.logger import Logger

logger = Logger(__name__).get_logger()


@when('the user navigates to "Dynamic Properties" section under "Elements"')
def step_navigate_to_dynamic_properties(context):
    """Navigate to Dynamic Properties section."""
    try:
        context.home_page.navigate_to_menu_item("Dynamic Properties")
        time.sleep(1)
        context.dynamic_properties_page = DynamicPropertiesPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to navigate to Dynamic Properties: {e}")
        raise


@then('the user should be navigated to a URL containing "demoqa.com/dynamic-properties"')
def step_verify_dynamic_properties_url(context):
    """Verify Dynamic Properties URL."""
    try:
        context.dynamic_properties_page.wait_for_url_contains("demoqa.com/dynamic-properties")
        assert "demoqa.com/dynamic-properties" in context.dynamic_properties_page.get_current_url()
    except Exception as e:
        logger.error(f"Dynamic Properties URL verification failed: {e}")
        raise


@given("the user is on the Dynamic Properties page")
def step_verify_on_dynamic_properties_page(context):
    """Verify user is on Dynamic Properties page."""
    assert "demoqa.com/dynamic-properties" in context.dynamic_properties_page.get_current_url()


@when("the user loads the page")
def step_load_page(context):
    """Load the page."""
    context.dynamic_properties_page.refresh_page()
    time.sleep(1)


@then('the user waits fluently for the button with text "Visible After 5 Seconds" to be displayed')
def step_wait_for_button_visible(context):
    """Wait for button to be visible."""
    result = context.dynamic_properties_page.wait_for_visible_after_5_seconds_button(timeout=10)
    assert result, "Button 'Visible After 5 Seconds' did not appear within timeout"


@then('the button with text "Visible After 5 Seconds" should be visible on the page')
def step_verify_button_visible(context):
    """Verify button is visible."""
    assert context.dynamic_properties_page.is_visible_after_5_seconds_button_visible()


@when('the user captures the initial color of the "Color Change" button')
def step_capture_initial_color(context):
    """Capture initial button color."""
    context.initial_text_color = context.dynamic_properties_page.get_color_change_button_color()
    context.initial_bg_color = context.dynamic_properties_page.get_color_change_button_background_color()

    assert context.initial_text_color is not None, "Failed to get initial text color"
    assert context.initial_bg_color is not None, "Failed to get initial background color"


@when('the user waits for the "Color Change" button color to change')
def step_wait_for_color_change(context):
    """Wait for button color to change."""
    color_changed = context.dynamic_properties_page.wait_for_color_change(timeout=10, property_name="color")

    if not color_changed:
        color_changed = context.dynamic_properties_page.wait_for_color_change(
            timeout=1, property_name="background-color"
        )

    assert color_changed, "Button color did not change within timeout period"


@then('the "Color Change" button should have a different color than initially')
def step_verify_color_changed(context):
    """Verify button color has changed from initial state."""
    final_text_color = context.dynamic_properties_page.get_color_change_button_color()
    final_bg_color = context.dynamic_properties_page.get_color_change_button_background_color()

    text_color_changed = final_text_color != context.initial_text_color
    bg_color_changed = final_bg_color != context.initial_bg_color

    assert text_color_changed or bg_color_changed, (
        f"No color change detected! Text: {context.initial_text_color} -> {final_text_color}, "
        f"Background: {context.initial_bg_color} -> {final_bg_color}"
    )
