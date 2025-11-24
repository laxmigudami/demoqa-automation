"""
Retry decorator for handling flaky test scenarios.
"""
import functools
import time
from typing import Any, Callable, Optional, Tuple, Type

from config.config import get_config
from utils.logger import Logger

config = get_config()
logger = Logger(__name__).get_logger()


def retry_on_failure(
    max_attempts: Optional[int] = None,
    delay: Optional[float] = None,
    exceptions: Tuple[Type[Exception], ...] = (AssertionError, Exception),
    backoff: float = 1.0,
) -> Callable:
    """
    Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of retry attempts (uses config.MAX_RETRIES if not specified)
        delay: Delay between retries in seconds (uses config.RETRY_DELAY if not specified)
        exceptions: Tuple of exception types to catch and retry
        backoff: Backoff multiplier for exponential backoff (1.0 = no backoff)

    Returns:
        Decorated function with retry capability

    Example:
        @retry_on_failure(max_attempts=3, delay=2)
        def flaky_step(context):
            assert context.page.is_loaded()
    """
    # Use config values if not specified
    max_attempts = max_attempts or config.MAX_RETRIES
    delay = delay or config.RETRY_DELAY

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            f"Function '{func.__name__}' failed after {max_attempts} attempts. " f"Last error: {str(e)}"
                        )
                        raise

                    logger.warning(
                        f"Function '{func.__name__}' failed on attempt {attempt}/{max_attempts}. "
                        f"Retrying in {current_delay}s... Error: {str(e)}"
                    )

                    time.sleep(current_delay)

                    # Apply backoff for exponential retry delay
                    if backoff > 1.0:
                        current_delay *= backoff

            # This should never be reached, but just in case
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def retry_on_stale_element(max_attempts: int = 3, delay: float = 0.5) -> Callable:
    """
    Decorator specifically for retrying on StaleElementReferenceException.

    Common in Selenium when DOM updates between finding and interacting with elements.

    Args:
        max_attempts: Maximum retry attempts (default: 3)
        delay: Delay between retries in seconds (default: 0.5)

    Returns:
        Decorated function with stale element retry capability

    Example:
        @retry_on_stale_element()
        def click_dynamic_button(self):
            self.driver.find_element(*locator).click()
    """
    from selenium.common.exceptions import StaleElementReferenceException

    return retry_on_failure(max_attempts=max_attempts, delay=delay, exceptions=(StaleElementReferenceException,))


def retry_with_refresh(max_attempts: int = 2, delay: float = 1.0) -> Callable:
    """
    Decorator that refreshes the page on failure before retrying.

    Useful for scenarios where page state might be corrupted.

    Args:
        max_attempts: Maximum retry attempts (default: 2)
        delay: Delay after refresh before retry (default: 1.0)

    Returns:
        Decorated function with page refresh capability

    Example:
        @retry_with_refresh(max_attempts=2)
        def verify_element_displayed(context):
            assert context.page.is_element_visible()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            f"Function '{func.__name__}' failed after {max_attempts} attempts "
                            f"with page refresh. Last error: {str(e)}"
                        )
                        raise

                    logger.warning(
                        f"Function '{func.__name__}' failed on attempt {attempt}/{max_attempts}. "
                        f"Refreshing page and retrying... Error: {str(e)}"
                    )

                    # Try to refresh page (assuming first arg is context with driver)
                    try:
                        if args and hasattr(args[0], "driver"):
                            args[0].driver.refresh()
                            time.sleep(delay)
                    except Exception as refresh_error:
                        logger.error(f"Page refresh failed: {refresh_error}")

            if last_exception:
                raise last_exception

        return wrapper

    return decorator


# Convenience decorator using config values
retry = retry_on_failure()
