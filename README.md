# DemoQA Test Automation Framework

## Overview

This is a comprehensive test automation framework I've built for web application testing, leveraging BDD principles to bridge the gap between technical and non-technical team members. The framework uses Python with Selenium WebDriver and Behave to create a maintainable and scalable testing solution that grows with your project needs.

## What Makes This Framework Effective

### Behavior-Driven Development Approach
I've implemented BDD using Gherkin syntax, which means anyone on the team—developers, QAs, or business analysts—can read and understand what's being tested. The Behave framework handles the Python implementation, making it easy to write tests in plain English that actually mean something to stakeholders.

### Page Object Model Architecture
The framework follows POM design pattern to keep things organized. UI elements and actions are separated from test logic, which means when the UI changes (and it always does), you only need to update one place. This has saved me countless hours of maintenance work on previous projects.

### Intelligent Wait Strategies
Rather than using hard-coded sleep statements that make tests slow and unreliable, I've implemented explicit and fluent waits that intelligently wait for elements to be ready. The framework also includes retry logic for those occasional flaky elements we all know and love.

### Rich Test Reporting
Allure reports give you a clear picture of what's happening with your tests. You get interactive HTML reports with screenshots attached to failures, detailed execution logs, and trend analysis over time. This makes it much easier to communicate test results to the team and track quality metrics.

### API and UI Testing Combined
The framework isn't just for UI testing. I've integrated API validation so you can verify that what you see in the UI matches what the backend is actually returning. This catches integration issues early.

---

## Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.8+ | Core programming language |
| **Web Automation** | Selenium WebDriver | 4.15.2 | Browser automation |
| **BDD Framework** | Behave | 1.2.6 | BDD implementation for Python |
| **Test Reporting** | Allure | 2.13.2 | Interactive HTML reports |
| **API Testing** | Requests | 2.31.0 | HTTP library for REST API validation |
| **WebDriver Management** | WebDriver Manager | 4.0.1 | Automatic browser driver management |
| **Configuration** | python-dotenv | 1.0.0 | Environment-based configuration |

---

## Framework Architecture

### How I've Structured the Tests

**Test Independence**: Each scenario can run independently and in any order. This is crucial for parallel execution and debugging specific failures.

**Clear Structure**: All scenarios follow the Given-When-Then format, making them easy to read and understand at a glance.

**Reusability**: Common steps are shared across features, so you write them once and use them everywhere.

**Organized Code**: Test logic, page objects, and utilities are clearly separated. Locators are centralized in one place, and configuration is externalized so you can easily change environments.

**Built for Reliability**: The framework uses explicit waits instead of sleep statements, includes retry logic for handling transient failures, and validates browser sessions to recover from unexpected issues.

---

## Framework Structure

```
demoqa_automation/
│
├── config/                          # Configuration Layer
│   ├── __init__.py
│   ├── config.py                    # Central configuration
│   └── browser_manager.py           # WebDriver management
│
├── features/                        # BDD Test Scenarios (Gherkin)
│   ├── *.feature                    # Feature files
│   ├── environment.py               # Behave hooks
│   └── steps/                       # Step Definitions
│       ├── common_steps.py          # Reusable steps
│       └── *_steps.py               # Feature-specific steps
│
├── pages/                           # Page Object Model Layer
│   ├── base_page.py                 # Base class with common methods
│   ├── locators.py                  # Centralized locator repository
│   └── *_page.py                    # Page-specific classes
│
├── utils/                           # Utility Modules
│   ├── api_client.py                # REST API client
│   ├── screenshot_handler.py        # Screenshot capture
│   └── retry_decorator.py           # Retry decorator
│
├── logs/                            # Execution Logs
├── reports/                         # Test Reports & Artifacts
│   ├── allure_reports/              # Allure JSON results
│   ├── allure_html/                 # Generated HTML reports
│   └── screenshots/                 # Failure screenshots
│
├── behave.ini                       # Behave configuration
├── requirements.txt                 # Python dependencies
├── run_tests.py                     # Test runner
└── pyproject.toml                   # Project configuration
```

---

## Test Coverage

I've maintained full traceability between requirements and test cases to ensure nothing falls through the cracks:

| Requirement | What We're Testing | Test Cases | Status |
|-------------|-------------------|------------|---------|
| Checkbox Tree - Dynamic Expansion | Tree expansion, cascading selection, state management | TC001-TC004 | Automated |
| Dynamic Properties - Visibility & State | Delayed element appearance, dynamic color changes | TC005-TC006 | Automated |
| Practice Forms - Field Validation | Mandatory fields, input validation, format checking | TC007-TC011 | Automated |
| Book Store - API Integration | UI-API data consistency, search functionality | TC012-TC013 | Automated |

**Current Coverage**: All 13 identified requirements have corresponding automated tests. This gives us 100% automation coverage across the tested features.

---

## What You'll Need

Before getting started, make sure you have these installed:

| Software | Version | Why You Need It |
|----------|---------|-----------------|
| Python | 3.8 or higher | The framework runs on Python |
| pip | 24.0.0 or higher | For installing dependencies |
| Git | Latest stable | To clone the repository |
| Chrome or Firefox | Latest stable | The browser where tests will run |
| Allure CLI | 2.13.0 or higher | Optional, but recommended for viewing reports |

Quick check to verify your setup:

```powershell
python --version
pip --version
git --version
```

---

## Getting Started

### Step 1: Clone the Repository

```powershell
git clone https://github.com/your-username/demoqa_automation.git
cd demoqa_automation
```

### Step 2: Set Up Virtual Environment

I always recommend using a virtual environment to keep dependencies isolated:

```powershell
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` in your terminal prompt when it's activated.

### Step 3: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs everything you need: Selenium, Behave, Allure, and other supporting libraries.

### Step 4: Verify Everything Works

```powershell
behave --version
python run_tests.py --help
```

If both commands run without errors, you're good to go!

### Step 5: Configure (Optional)

The framework works out of the box with sensible defaults, but you can customize settings by creating a `.env` file:

```env
BROWSER=chrome              # Options: chrome, firefox, edge
HEADLESS=false             # Set to true for headless execution
BASE_URL=https://demoqa.com
IMPLICIT_WAIT=10           # Default wait time in seconds
EXPLICIT_WAIT=15
LOG_LEVEL=INFO             # Options: DEBUG, INFO, WARNING, ERROR
```

---

## Running Your Tests

### Run Everything

The simplest way to run all tests:

```powershell
python run_tests.py
```

This executes the full test suite and generates Allure reports automatically.

### Run Specific Features

When you're working on a particular feature, you can run just those tests:

```powershell
# Checkbox tests only
python run_tests.py --features="features/checkbox_tree_dynamic_expansion_and_validation.feature"

# Form validation tests
python run_tests.py --features="features/practice_forms_field_validation.feature"
```

### Run by Tags

I've tagged tests by type and priority so you can run subsets:

```powershell
# Quick smoke tests
python run_tests.py --tags="@smoke"

# All functional tests
python run_tests.py --tags="@functional"

# Critical priority tests only
python run_tests.py --tags="@critical"

# Combine tags
python run_tests.py --tags="@smoke and @functional"
```

### Using Behave Directly

You can also use Behave commands directly if you prefer:

```powershell
# Run all features
behave features/

# Run a specific scenario by name
behave -n "TC001 - Dynamically expand the tree at all levels"

# Dry run to validate scenarios without execution
behave --dry-run features/
```

---

## Test Reports with Allure

### Setting Up Allure (One-Time Setup)

If you haven't installed Allure CLI yet, here are two ways to do it:

**Option 1: Manual Installation**
1. Download the latest release from [Allure Releases](https://github.com/allure-framework/allure2/releases)
2. Extract it to `C:\allure\`
3. Add `C:\allure\allure-2.24.0\bin` to your System PATH
4. Verify with `allure --version`

**Option 2: Using Scoop (easier)**
```powershell
scoop install allure
allure --version
```

### Viewing Your Test Reports

After running tests, view the results:

```powershell
# Quick view - opens report in browser automatically
allure serve reports/allure_reports

# Generate a permanent HTML report
allure generate reports/allure_reports -o reports/allure_html --clean
allure open reports/allure_html
```

### Sample Allure Report

![Allure Report Overview](<Screenshot 2025-11-24 051142.png>)

The Allure report provides a comprehensive view with pass/fail statistics, execution timeline, detailed step breakdowns, and automatic screenshot attachments for failures.

### How Tests Are Distributed

I've covered different testing aspects:
- **Functional Testing**: Core feature validation (6 tests)
- **Integration Testing**: UI-API consistency checks (2 tests)
- **Data-Driven Testing**: Multiple inputs per scenario (2 tests)
- **Negative Testing**: Invalid inputs and error handling (2 tests)
- **Boundary Testing**: Input limits and edge cases (1 test)

---

## Tips and Troubleshooting

### Customizing Configuration

You can adjust these settings in your `.env` file or `config/config.py`:

**Browser Settings:**
- Choose your browser: chrome, firefox, or edge
- Run headless (faster, no GUI): set HEADLESS=true

**Wait Times:**
- IMPLICIT_WAIT: 10 seconds (general waiting)
- EXPLICIT_WAIT: 15 seconds (specific elements)
- FLUENT_WAIT: 20 seconds (polling for dynamic elements)
- POLL_FREQUENCY: 0.5 seconds (how often to check)

**Logging:**
- Control verbosity: DEBUG (detailed), INFO (standard), WARNING, ERROR
- Enable/disable file and console output

### When Tests Fail

Here's my debugging process:

```powershell
# First, check the logs
type logs\behave_execution.log

# Look at the failure screenshot
explorer reports\screenshots

# Run just that one failing test
behave -n "TC001 - Dynamically expand the tree at all levels"

# Enable debug logging for more details
# (Set LOG_LEVEL=DEBUG in config)
```

### Running Tests Faster

For local development or CI/CD pipelines:

```powershell
# Run in headless mode (no browser GUI)
# Set HEADLESS=true in config

# Run only critical tests
python run_tests.py --tags="@critical or @smoke"
```

### Keeping the Framework Healthy

```powershell
# Check code quality
black .
flake8 .
pylint pages/ utils/ config/

# See which dependencies are outdated
pip list --outdated

# Update specific packages
pip install --upgrade selenium
```

---

## Need Help?

If you run into issues, here's what helps me troubleshoot:

- Which Python version you're using (`python --version`)
- Your browser and its version
- The full error message from the logs
- Any screenshots from failed tests
- What you were trying to do when it failed

Check the `logs/` directory for detailed execution logs, and `reports/screenshots/` for visual evidence of failures.

---
