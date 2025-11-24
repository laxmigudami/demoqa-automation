import logging
import sys
from datetime import datetime

from config.config import get_config

config = get_config()


class Logger:
    """
    Simple logger for test automation framework.
    Provides console and file logging with execution tracking.
    """

    _loggers = {}
    _execution_log_file = None

    def __init__(self, name):
        """Initialize logger with given name."""
        self.name = name
        self.logger = self._get_logger(name)

    @classmethod
    def _setup_execution_logger(cls):
        """Setup main execution logger."""
        if cls._execution_log_file is None:
            config.LOGS_PATH.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cls._execution_log_file = config.LOGS_PATH / f"test_execution_{timestamp}.log"

    @classmethod
    def _get_logger(cls, name):
        """Get or create logger instance."""
        cls._setup_execution_logger()

        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, config.LOG_LEVEL))
        logger.handlers.clear()
        logger.propagate = False

        config.LOGS_PATH.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Module-specific file handler
        log_file = config.LOGS_PATH / f"{name.replace('.', '_')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Execution log handler
        exec_handler = logging.FileHandler(cls._execution_log_file, encoding="utf-8")
        exec_handler.setLevel(logging.DEBUG)
        exec_handler.setFormatter(formatter)
        logger.addHandler(exec_handler)

        cls._loggers[name] = logger
        return logger

    def get_logger(self):
        """Get logger instance."""
        return self.logger

    @classmethod
    def get_execution_log_file(cls):
        """Get the path to current execution log file."""
        return cls._execution_log_file


def get_logger(name):
    """
    Get logger instance.

    Args:
        name: Logger name (use __name__)

    Returns:
        Logger instance
    """
    return Logger(name).get_logger()


def get_execution_log_path():
    """Get the current execution log file path."""
    return Logger.get_execution_log_file()


class BehaveLogger:
    """Logging utility for Behave test execution."""

    def __init__(self):
        self.logger = get_logger("behave.execution")
        self.scenario_count = 0

    def log_execution_start(self, config, log_path):
        """Log test execution initialization."""
        self.logger.info("Test execution started")
        self.logger.info(f"Base URL: {config.BASE_URL}")
        self.logger.info(f"Browser: {config.BROWSER} (Headless: {config.HEADLESS})")
        self.logger.info(f"Log file: {log_path}")
        self.logger.info("-" * 80)

    def log_webdriver_init(self):
        """Log WebDriver initialization."""
        self.logger.info("WebDriver initialized successfully")

    def log_scenario_start(self, scenario):
        """Log scenario execution start."""
        self.scenario_count += 1
        self.logger.info(f"Scenario #{self.scenario_count}: {scenario.name}")
        self.logger.info(f"Feature: {scenario.feature.name}")
        if scenario.tags:
            self.logger.info(f"Tags: {', '.join(scenario.tags)}")

    def log_scenario_end(self, scenario, duration, tc_id=None):
        """Log scenario execution result."""
        if scenario.status == "passed":
            self.logger.info(f"Scenario passed: {scenario.name} (Duration: {duration:.2f}s)")
        elif scenario.status == "failed":
            self.logger.error(f"Scenario failed: {scenario.name} (Duration: {duration:.2f}s)")
        elif scenario.status == "skipped":
            self.logger.warning(f"Scenario skipped: {scenario.name}")
        else:
            self.logger.error(f"Scenario error: {scenario.name} (Duration: {duration:.2f}s)")

        self.logger.info("-" * 80)

    def log_screenshot_captured(self, path):
        """Log screenshot capture."""
        self.logger.info(f"Screenshot saved: {path}")

    def log_execution_summary(self, results, total_duration):
        """Log final test execution summary."""
        total = sum(len(v) for v in results.values())
        passed = len(results["passed"])
        failed = len(results["failed"])
        errors = len(results["error"])
        skipped = len(results["skipped"])

        pass_rate = (passed / total * 100) if total > 0 else 0

        self.logger.info("=" * 80)
        self.logger.info("TEST EXECUTION SUMMARY")
        self.logger.info("=" * 80)
        self.logger.info(f"Total scenarios: {total}")
        self.logger.info(f"Passed: {passed} ({passed / total * 100:.1f}%)" if total > 0 else f"Passed: {passed}")
        self.logger.info(f"Failed: {failed} ({failed / total * 100:.1f}%)" if total > 0 else f"Failed: {failed}")
        self.logger.info(f"Errors: {errors} ({errors / total * 100:.1f}%)" if total > 0 else f"Errors: {errors}")
        self.logger.info(f"Skipped: {skipped} ({skipped / total * 100:.1f}%)" if total > 0 else f"Skipped: {skipped}")
        self.logger.info(f"Pass rate: {pass_rate:.2f}%")
        self.logger.info(f"Total duration: {total_duration:.2f}s ({total_duration / 60:.2f} min)")
        self.logger.info("=" * 80)

        if failed > 0 or errors > 0:
            self._log_failed_scenarios(results)

    def _log_failed_scenarios(self, results):
        """Log details of failed scenarios."""
        if results["failed"]:
            self.logger.info("Failed scenarios:")
            for i, test in enumerate(results["failed"], 1):
                name = self._clean_test_name(test)
                self.logger.info(f"  {i}. {test['id']} - {name} ({test.get('duration', 0):.2f}s)")

        if results["error"]:
            self.logger.info("Scenarios with errors:")
            for i, test in enumerate(results["error"], 1):
                name = self._clean_test_name(test)
                self.logger.info(f"  {i}. {test['id']} - {name} ({test.get('duration', 0):.2f}s)")

    def _clean_test_name(self, test):
        """Remove test ID prefix from scenario name."""
        name = test["name"]
        if " - " in name:
            return name.split(" - ", 1)[1]
        return name

    def log_artifacts_location(self, config):
        """Log location of generated artifacts."""
        self.logger.info("Generated artifacts:")
        self.logger.info(f"  Reports: {config.REPORTS_PATH / 'allure_reports'}")
        self.logger.info(f"  Screenshots: {config.SCREENSHOTS_PATH}")
        self.logger.info(f"  Logs: {config.LOGS_PATH}")

    def log_execution_end(self, results, total_duration):
        """Log test execution end (alias for log_execution_summary)."""
        self.log_execution_summary(results, total_duration)

    def log_execution_complete(self, success):
        """Log execution completion status."""
        if success:
            self.logger.info("All tests passed successfully")
        else:
            self.logger.warning("Some tests failed - review logs for details")

        self.logger.info("Test execution finished")
        self.logger.info("=" * 80)

    def log_webdriver_closed(self):
        """Log WebDriver cleanup."""
        self.logger.info("WebDriver closed successfully")
