import pytest
from automation.api.strings_api import ApiClient


def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="http://127.0.0.1:8000/",
        help="Base URL for the API client."
    )

    parser.addoption(
        "--request-debug",
        action="store_true",
        default=True,
        help="Enable request debugging output."
    )


@pytest.fixture
def api_client(request) -> ApiClient:
    """
    Fixture to provide an instance of ApiClient for tests.

    Returns:
        ApiClient: An instance of the ApiClient.
    """
    url: str = request.config.getoption("--api-url")
    request_debug: str = request.config.getoption("--request-debug")
    hooks: dict[str, list] = {}

    if request_debug:
        hooks['response'] = [lambda r, *args, **kwargs: print(f"Response: {r.status_code} {r.text}")]

    return ApiClient(base_url=url, hooks=hooks)


pytest_plugins = [
    "automation.plugin.pytest_docker_plugin"
]
