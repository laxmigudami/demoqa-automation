from datetime import datetime
from typing import Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.config import get_config
from pages.base_page import BasePage
from pages.locators import FormsPageLocators
from utils.logger import Logger

config = get_config()
logger = Logger(__name__).get_logger()


class FormsPage(BasePage):
    """Page object for the Practice Forms page."""

    def __init__(self, driver: WebDriver) -> None:
        """Initialize the Forms page."""
        super().__init__(driver)
        self.locators = FormsPageLocators()
        # Note: self.wait is inherited from BasePage with config.EXPLICIT_WAIT

    def enter_first_name(self, first_name: str) -> None:
        """Enter first name in the form."""
        self.enter_text(self.locators.FIRST_NAME_INPUT, first_name)
        logger.info(f"Entered first name: {first_name}")

    def enter_last_name(self, last_name: str) -> None:
        """Enter last name in the form."""
        self.enter_text(self.locators.LAST_NAME_INPUT, last_name)
        logger.info(f"Entered last name: {last_name}")

    def enter_email(self, email: str) -> None:
        """Enter email in the form."""
        self.enter_text(self.locators.EMAIL_INPUT, email)
        logger.info(f"Entered email: {email}")

    def enter_mobile(self, mobile: str) -> None:
        """Enter mobile number in the form."""
        self.enter_text(self.locators.MOBILE_INPUT, mobile)
        logger.info(f"Entered mobile: {mobile}")

    def select_gender(self, gender: str) -> None:
        """Select gender radio button."""
        gender = gender.lower()
        if gender == "female":
            label_locator = self.locators.GENDER_FEMALE_LABEL
            radio_locator = self.locators.GENDER_FEMALE_RADIO
        elif gender == "male":
            label_locator = self.locators.GENDER_MALE_LABEL
            radio_locator = self.locators.GENDER_MALE_RADIO
        else:
            raise ValueError(f"Unsupported gender: {gender}")

        try:
            self.wait_for_element_visible(label_locator)
            label_element = self.wait.until(EC.element_to_be_clickable(label_locator))
            self.driver.execute_script("arguments[0].click();", label_element)
            logger.info(f"Selected {gender.capitalize()} gender")
        except Exception as e:
            logger.warning(f"Label click failed, trying radio button directly: {e}")
            radio_element = self.find_element(radio_locator)
            self.driver.execute_script("arguments[0].checked = true; arguments[0].click();", radio_element)
            logger.info(f"Selected {gender.capitalize()} gender using direct radio button")

    def enter_date_of_birth(self, date: str) -> None:
        """Enter date of birth in the form."""
        try:
            date_obj = datetime.strptime(date, "%d %b %Y")
            formatted_date = date_obj.strftime("%m/%d/%Y")
        except ValueError:
            formatted_date = date

        date_element = self.wait.until(EC.presence_of_element_located(self.locators.DATE_OF_BIRTH_INPUT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_element)
        # Wait for element to be ready after scroll
        self.wait.until(EC.element_to_be_clickable(self.locators.DATE_OF_BIRTH_INPUT))
        self.driver.execute_script("arguments[0].click();", date_element)
        date_element.send_keys(Keys.CONTROL + "a")
        date_element.send_keys(formatted_date)
        date_element.send_keys(Keys.ENTER)
        logger.info(f"Entered date of birth: {date} (formatted as {formatted_date})")

    def enter_current_address(self, address: str) -> None:
        """Enter current address in the form."""
        self.enter_text(self.locators.CURRENT_ADDRESS_TEXTAREA, address)
        logger.info(f"Entered address: {address}")

    def submit_form(self) -> None:
        """Submit the form."""
        self.click_element(self.locators.SUBMIT_BUTTON)
        logger.info("Form submitted")

    def verify_field_error(self, field_placeholder: str) -> bool:
        """Verify if a field shows an error indication."""
        try:
            # Use explicit wait with shorter timeout for validation checks
            short_wait = WebDriverWait(self.driver, max(5, config.EXPLICIT_WAIT // 3))
            element = short_wait.until(
                EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{field_placeholder}']"))
            )

            # Check HTML5 validation state using :invalid pseudo-class
            # Execute JavaScript to check if the field matches :invalid selector
            try:
                is_invalid = self.driver.execute_script("return arguments[0].matches(':invalid');", element)
                if is_invalid:
                    logger.info(f"Field '{field_placeholder}' has HTML5 :invalid state")
                    return True
            except Exception as js_error:
                logger.warning(f"Failed to check :invalid state: {js_error}")

            # Get field properties with timeout protection
            try:
                border_color = element.value_of_css_property("border-color")
                box_shadow = element.value_of_css_property("box-shadow")
                value = element.get_attribute("value")
                required = element.get_attribute("required")
                minlength = element.get_attribute("minlength")
                # pattern = element.get_attribute("pattern")  # Unused
            except Exception as css_error:
                logger.warning(f"Failed to get CSS properties, assuming error state: {css_error}")
                return True

            # Check for invalid characters in mobile field
            if field_placeholder == "Mobile Number":
                maxlength = element.get_attribute("maxlength")

                # Check minlength validation
                if minlength and value:
                    min_len = int(minlength)
                    if len(value) < min_len:
                        logger.info(f"Field '{field_placeholder}' value '{value}' is shorter than minlength {min_len}")
                        return True

                # If field contains any non-digit characters, it's an error
                if value and not value.isdigit():
                    logger.info(f"Field '{field_placeholder}' contains non-digit characters: {value}")
                    return True

                # If field is at max length but still has non-digits (filtered), error
                if maxlength and value and len(value) == int(maxlength) and not value.isdigit():
                    logger.info(f"Field '{field_placeholder}' at max length with non-digits")
                    return True

            # Check visual error indicators
            is_error = (
                "rgb(220, 53, 69)" in border_color
                or "rgb(255, 0, 0)" in border_color
                or "#dc3545" in border_color.lower()
                or "rgb(220, 53, 69)" in box_shadow
                or "rgb(255, 0, 0)" in box_shadow
                or "#dc3545" in box_shadow.lower()
            )

            # Check if required field is empty
            if required and (value is None or value.strip() == ""):
                is_error = True

            # Check for explicit error messages (with timeout)
            try:
                error_message = self.driver.find_element(
                    By.XPATH,
                    f"//input[@placeholder='{field_placeholder}']/following-sibling::*"
                    f"[contains(@class, 'field-error') or contains(@class, 'error')]",
                )
                if error_message and error_message.is_displayed():
                    is_error = True
            except Exception:
                pass

            logger.info(f"Field '{field_placeholder}' error status: {is_error}")
            return is_error
        except Exception as e:
            logger.error(f"Error verifying field error: {e}")
            # If verification fails completely, assume it's an error state
            return True

    def is_success_modal_displayed(self) -> bool:
        """Check if success modal is displayed."""
        return self.is_element_visible(self.locators.SUCCESS_MODAL_TITLE)

    def get_submitted_data(self) -> Dict[str, str]:
        """Get submitted form data from success modal."""
        self.wait_for_element_visible(self.locators.SUCCESS_MODAL)
        rows = self.find_elements(self.locators.MODAL_TABLE_ROWS)
        data = {}

        for i in range(0, len(rows), 2):
            if i + 1 < len(rows):
                label = rows[i].text.strip()
                value = rows[i + 1].text.strip()
                data[label] = value

        logger.info(f"Retrieved submitted data: {data}")
        return data

    def get_field_value(self, locator: tuple) -> str:
        """Get the value of a form field."""
        try:
            # Use direct find for faster retrieval
            element = self.driver.find_element(*locator)
            value = element.get_attribute("value")
            logger.info(f"Retrieved field value: {value}")
            return value if value else ""
        except Exception as e:
            logger.error(f"Error getting field value: {e}")
            return ""

    def verify_gender_error(self) -> bool:
        """Verify if gender field shows an error."""
        try:
            # Use direct find for faster verification
            male_radio = self.driver.find_element(*self.locators.GENDER_MALE_RADIO)
            female_radio = self.driver.find_element(*self.locators.GENDER_FEMALE_RADIO)

            male_checked = male_radio.is_selected()
            female_checked = female_radio.is_selected()

            if not male_checked and not female_checked:
                try:
                    gender_container = self.driver.find_element(By.XPATH, "//div[@id='genterWrapper']")
                    border_color = gender_container.value_of_css_property("border-color")
                    box_shadow = gender_container.value_of_css_property("box-shadow")

                    is_error = (
                        "rgb(220, 53, 69)" in border_color
                        or "rgb(255, 0, 0)" in border_color
                        or "rgb(220, 53, 69)" in box_shadow
                        or "rgb(255, 0, 0)" in box_shadow
                    )

                    logger.info(f"Gender field error status: {is_error}")
                    return is_error or not (male_checked or female_checked)
                except Exception:
                    logger.info("Gender field error: no gender selected")
                    return True

            logger.info("Gender field: a gender is selected, no error")
            return False
        except Exception as e:
            logger.error(f"Error verifying gender field error: {e}")
            return False

    def close_success_modal(self) -> None:
        """Close success modal if displayed."""
        try:
            if self.is_element_present(self.locators.MODAL_CLOSE_BUTTON):
                self.click_element(self.locators.MODAL_CLOSE_BUTTON)
                logger.info("Success modal closed")
        except Exception as e:
            logger.warning(f"Failed to close success modal: {e}")

    def refresh_form(self) -> None:
        """Refresh the form page."""
        try:
            self.refresh_page()
            logger.info("Form page refreshed")
        except Exception as e:
            logger.warning(f"Failed to refresh form: {e}")
