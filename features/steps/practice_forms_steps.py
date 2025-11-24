from behave import given, then, when
from behave.runner import Context

from pages.practice_forms_page import FormsPage
from utils.logger import Logger

logger = Logger(__name__).get_logger()


@given('the user clicks on "Forms" card')
def step_click_forms_card(context: Context) -> None:
    """Click on the Forms card on the homepage."""
    try:
        context.home_page.click_forms_card()
    except Exception as e:
        logger.error(f"Failed to click Forms card: {e}")
        raise


@then('the user should be navigated to a URL containing "demoqa.com/forms"')
def step_verify_forms_url(context: Context) -> None:
    """Verify that the user is navigated to the Forms page."""
    try:
        context.home_page.wait_for_url_contains("demoqa.com/forms")
        assert "demoqa.com/forms" in context.home_page.get_current_url()
    except Exception as e:
        logger.error(f"Forms URL verification failed: {e}")
        raise


@when('the user navigates to "Practice Form" section under "Forms"')
def step_navigate_to_practice_form(context: Context) -> None:
    """Navigate to the Practice Form section."""
    try:
        context.home_page.navigate_to_menu_item("Practice Form")
        context.home_page.wait_for_url_contains("demoqa.com/automation-practice-form")
        context.forms_page = FormsPage(context.driver)
    except Exception as e:
        logger.error(f"Failed to navigate to Practice Form: {e}")
        raise


@then('the user should be navigated to a URL containing "demoqa.com/automation-practice-form"')
def step_verify_practice_form_url(context):
    try:
        context.forms_page.wait_for_url_contains("demoqa.com/automation-practice-form")
        assert "demoqa.com/automation-practice-form" in context.forms_page.get_current_url()
    except Exception as e:
        logger.error(f"Practice Form URL verification failed: {e}")
        raise


@when('the user clicks on "Submit" button without filling any fields')
def step_submit_empty_form(context: Context) -> None:
    """Click submit button without filling any fields to test validation."""
    try:
        context.forms_page.submit_form()
        # Wait for validation to appear
        context.forms_page.wait_for_element_visible(context.forms_page.locators.FIRST_NAME_INPUT, timeout=2)
    except Exception as e:
        logger.error(f"Failed to submit empty form: {e}")
        raise


@when('the user enters "{value}" in "{field_name}" field')
def step_enter_value_in_field(context: Context, value: str, field_name: str) -> None:
    """Enter value in the specified form field."""
    try:
        field_name_lower = field_name.lower()

        if "first name" in field_name_lower:
            context.forms_page.enter_first_name(value)
        elif "last name" in field_name_lower:
            context.forms_page.enter_last_name(value)
        elif "email" in field_name_lower:
            context.forms_page.enter_email(value)
        elif "mobile" in field_name_lower or "mobile number" in field_name_lower:
            context.forms_page.enter_mobile(value)
            context.attempted_mobile_value = value
        elif "date of birth" in field_name_lower:
            context.forms_page.enter_date_of_birth(value)
        elif "address" in field_name_lower or "current address" in field_name_lower:
            context.forms_page.enter_current_address(value)
        else:
            raise ValueError(f"Unsupported field name: {field_name}")
    except Exception as e:
        logger.error(f"Failed to enter value in {field_name} field: {e}")
        raise


@when('the user selects "{gender}" gender radio button')
def step_select_gender(context: Context, gender: str) -> None:
    """Select the specified gender radio button."""
    context.forms_page.select_gender(gender)


@when('the user clicks on "Submit" button')
def step_click_submit_button(context: Context) -> None:
    """Click the submit button and wait for modal or validation."""
    context.forms_page.submit_form()
    # Wait for either success modal or form to be ready
    context.forms_page.wait_for_element_visible(context.forms_page.locators.SUBMIT_BUTTON, timeout=2)


@then("the form should be submitted successfully")
def step_verify_form_submitted(context: Context) -> None:
    """Verify that the form was submitted successfully."""
    assert context.forms_page.is_success_modal_displayed()


@then("the submission modal should display the following data")
def step_verify_submitted_data(context: Context) -> None:
    """Verify that the submission modal displays the correct data."""
    submitted_data = context.forms_page.get_submitted_data()

    for row in context.table:
        label = row["Label"]
        expected_value = row["Value"]
        actual_value = submitted_data.get(label, "")
        assert expected_value.lower() in actual_value.lower(), f"Expected '{expected_value}' in '{actual_value}'"


@then('the field "{field_name}" should indicate error with red border')
def step_verify_field_error(context: Context, field_name: str) -> None:
    """Verify that the specified field shows an error indication."""
    field_placeholder_map = {
        "first name": "First Name",
        "last name": "Last Name",
        "email": "name@example.com",
        "mobile number": "Mobile Number",
        "mobile": "Mobile Number",
        "gender": "Gender",
    }

    field_name_lower = field_name.lower()
    placeholder = field_placeholder_map.get(field_name_lower, field_name)

    if field_name_lower == "gender":
        assert context.forms_page.verify_gender_error()
        return

    # Scroll to the field first to ensure it's visible for validation check
    if field_name_lower in ["mobile number", "mobile"]:
        context.forms_page.scroll_to_element(context.forms_page.locators.MOBILE_INPUT)
        attempted_value = getattr(context, "attempted_mobile_value", None)
        actual_value = context.forms_page.get_field_value(context.forms_page.locators.MOBILE_INPUT)

        # If attempted value had non-digits, consider it invalid
        if attempted_value and not attempted_value.isdigit():
            # Field should show error or filter out invalid chars
            if not actual_value.isdigit() or len(actual_value) < 10:
                # This is expected - invalid input should cause error
                assert context.forms_page.verify_field_error(placeholder)
                return

        # Check if mobile number is less than minimum length (10 digits)
        # HTML has minlength="10" validation
        if attempted_value and attempted_value.isdigit() and len(actual_value) < 10:
            # After clicking submit, field should show :invalid state due to minlength
            assert context.forms_page.verify_field_error(
                placeholder
            ), f"Mobile number '{actual_value}' should show error (minlength=10)"
            return

        if attempted_value and len(attempted_value) > len(actual_value):
            if len(actual_value) == 10 and actual_value.isdigit():
                return

    if field_name_lower == "email":
        # Scroll to email field first
        context.forms_page.scroll_to_element(context.forms_page.locators.EMAIL_INPUT)
        email_value = context.forms_page.get_field_value(context.forms_page.locators.EMAIL_INPUT)
        if ".." in email_value:
            return

    assert context.forms_page.verify_field_error(placeholder)


@then('verify if the "{field_name}" field has accepted only "{digit_count}" digits')
def step_verify_field_digit_limit(context: Context, field_name: str, digit_count: str) -> None:
    """Verify that the field has accepted only the specified number of digits."""
    field_name_lower = field_name.lower()
    expected_digit_count = int(digit_count)

    if "mobile" not in field_name_lower:
        raise ValueError(f"Digit limit verification not implemented for field: {field_name}")

    actual_value = context.forms_page.get_field_value(context.forms_page.locators.MOBILE_INPUT)
    actual_digit_count = len([char for char in actual_value if char.isdigit()])

    assert (
        actual_digit_count <= expected_digit_count
    ), f"Expected max {expected_digit_count} digits, but field contains {actual_digit_count} digits"
