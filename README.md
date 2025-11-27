# Kiwi.com Flight Search Automation

This project contains an automated test suite for the Kiwi.com flight search functionality using Python, Playwright, and Pytest with BDD (Behavior-Driven Development) principles.

## Project Structure

```
kiwi_tests/
├── features/             # Gherkin feature files
│   └── basic_search.feature
├── pages/                # Page Object Model definitions
│   └── home_page.py
└── steps/                # Step definitions for Gherkin scenarios
    └── basic_search_steps.py
.github/
└── workflows/
    └── playwright.yml    # GitHub Actions CI/CD workflow
Dockerfile                # Dockerfile for containerization
requirements.txt          # Python dependencies
README.md                 # Project README
CHANGELOG.md              # Project Changelog
```

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   (Optional) Docker for containerized execution

### Installation

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:stefanaonx/test-framework-playwright-pytest.git
    cd git@github.com:stefanaonx/test-framework-playwright-pytest.git
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**

    ```bash
    playwright install
    ```

## How to Run Tests

### Run All Tests

To run all tests in the suite:

```bash
pytest
```

### Run Specific Test Cases

#### By Marker

If a test scenario in the feature file is tagged (e.g., `@basic_search`), you can run it using the `-m` flag:

```bash
pytest -m basic_search
```

#### By File and Scenario Name

You can also specify the test file and the scenario function directly:

```bash
pytest kiwi_tests/steps/basic_search_steps.py::test_one_way_flight_search
```

### Run Tests in Headless Mode (Default)

Playwright runs in headless mode by default, meaning no browser UI will be shown during execution.

### Run Tests in Headful Mode (with UI)

To see the browser UI during test execution, use the `--headed` flag:

```bash
pytest --headed
```

## Docker Integration

This project includes a `Dockerfile` to enable running tests within a Docker container, ensuring a consistent environment.

### Build the Docker Image

```bash
docker build -t kiwi-tests .
```

### Run Tests in a Docker Container

To run all tests in the Docker container:

```bash
docker run kiwi-tests
```

To run a specific test (e.g., by marker) in the Docker container:

```bash
docker run kiwi-tests pytest -m basic_search
```

## CI/CD with GitHub Actions

This project is configured with GitHub Actions for continuous integration. The workflow defined in `.github/workflows/playwright.yml` will automatically run the tests on `push` and `pull_request` events to the `main` branch.

### Workflow Details

The `playwright.yml` workflow performs the following steps:

1.  **Checkout Code:** Retrieves the project code.
2.  **Setup Python:** Configures a Python 3.10 environment.
3.  **Install Dependencies:** Installs `pip` dependencies from `requirements.txt` and Playwright browsers.
4.  **Run Playwright Tests:** Executes all Pytest tests.

