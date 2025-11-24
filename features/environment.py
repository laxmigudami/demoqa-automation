from datetime import datetime

from behave.model import Scenario
from behave.runner import Context

from config.browser_manager import BrowserManager
from config.config import get_config
from utils.logger import BehaveLogger, get_execution_log_path
from utils.screenshot_handler import ScreenshotHandler

config = get_config()
behave_logger = BehaveLogger()


def before_all(context: Context) -> None:
    """Initialize test execution before all scenarios"""
    context.execution_start_time = datetime.now()
    context.behave_logger = behave_logger

    # Log execution start
    behave_logger.log_execution_start(config, get_execution_log_path())

    # Initialize WebDriver
    context.driver = BrowserManager.setup_browser()
    context.base_url = config.BASE_URL
    behave_logger.log_webdriver_init()

    # Initialize test tracking
    context.test_results = {"passed": [], "failed": [], "skipped": [], "error": []}


def before_scenario(context: Context, scenario: Scenario) -> None:
    """Run before each scenario"""
    context.scenario_start_time = datetime.now()
    context.scenario_name = scenario.name

    # Validate browser session and recreate if needed
    if not _is_browser_session_valid(context):
        behave_logger.logger.warning("Browser session invalid, recreating...")
        try:
            BrowserManager.teardown_browser(context.driver)
        except Exception:
            pass
        context.driver = BrowserManager.setup_browser()
        behave_logger.logger.info("Browser session recreated successfully")

    behave_logger.log_scenario_start(scenario)


def _is_browser_session_valid(context: Context) -> bool:
    """Check if the browser session is still valid"""
    if not hasattr(context, "driver") or context.driver is None:
        return False
    try:
        # Try to get current URL to verify session is alive
        _ = context.driver.current_url
        return True
    except Exception as e:
        behave_logger.logger.warning(f"Browser session validation failed: {e}")
        return False


def after_scenario(context: Context, scenario: Scenario) -> None:
    """Run after each scenario - cleanup and logging"""
    # Calculate scenario duration
    duration = (
        (datetime.now() - context.scenario_start_time).total_seconds() if hasattr(context, "scenario_start_time") else 0
    )

    # Extract test case ID from scenario name
    tc_id = scenario.name.split(" - ")[0] if " - " in scenario.name else scenario.name

    # Log scenario result
    behave_logger.log_scenario_end(scenario, duration, tc_id)

    # Track test results
    test_record = {"id": tc_id, "name": scenario.name, "duration": duration}

    if scenario.status == "passed":
        context.test_results["passed"].append(test_record)
    elif scenario.status == "failed":
        context.test_results["failed"].append(test_record)
        _capture_failure_screenshot(context, tc_id)
    elif scenario.status == "skipped":
        context.test_results["skipped"].append(test_record)
    else:
        context.test_results["error"].append(test_record)

    # Clean up scenario state (moved after logging to avoid errors)
    _cleanup_scenario_state(context)


def _cleanup_scenario_state(context: Context) -> None:
    """Clean up page state after scenario"""
    try:
        # Close success modal if open (forms page only)
        if hasattr(context, "forms_page"):
            try:
                context.forms_page.close_success_modal()
            except Exception:
                pass

        # Clean up API client session
        if hasattr(context, "api_client"):
            try:
                context.api_client.close()
                delattr(context, "api_client")
            except Exception:
                pass
    except Exception:
        pass


def _capture_failure_screenshot(context: Context, tc_id: str) -> None:
    """Capture screenshot on test failure"""
    if config.SCREENSHOT_ON_FAILURE and hasattr(context, "driver"):
        try:
            # Only capture screenshot if driver is still available
            if context.driver:
                screenshot_handler = ScreenshotHandler(context.driver)
                screenshot_path = screenshot_handler.take_screenshot(f"{tc_id}_FAILED")
                if screenshot_path:
                    behave_logger.log_screenshot_captured(screenshot_path)
        except Exception:
            pass


def after_all(context: Context) -> None:
    """Clean up after all scenarios"""
    # Generate final execution summary
    execution_time = (datetime.now() - context.execution_start_time).total_seconds()
    behave_logger.log_execution_end(context.test_results, execution_time)

    # Close driver
    if hasattr(context, "driver"):
        BrowserManager.teardown_browser(context.driver)
