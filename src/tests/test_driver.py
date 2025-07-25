from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from nodriver import Browser

from scraping_service.helpers.driver import DriverClient
from scraping_service.helpers.schemas import SearchResult

TEST_DATA_PATH = Path(__file__).parent / "test_data"
SEARCH_FILENAMES = [
    "search_AI.html",
    "search_Docker.html",
    "search_Kubernetes.html",
    "search_ML.html",
    "search_Python.html",
    "search_Rust.html",
]
NON_SEARCH_FILENAMES = [
    "rickroll.html",
]


@pytest.fixture()
def urls() -> list[str]:
    """Return the URLs of the test files."""
    return {
        "SEARCH_URLS": [
            "file://" + str(TEST_DATA_PATH / file_name)
            for file_name in SEARCH_FILENAMES
        ],
        "NON_SEARCH_URLS": [
            "file://" + str(TEST_DATA_PATH / file_name)
            for file_name in NON_SEARCH_FILENAMES
        ],
    }


@pytest.fixture()
def htmls() -> list[str]:
    """Return the HTML content of the test files."""
    return {
        "SEARCH_HTML": [
            (TEST_DATA_PATH / file_name).read_text() for file_name in SEARCH_FILENAMES
        ],
        "NON_SEARCH_HTML": [
            (TEST_DATA_PATH / file_name).read_text()
            for file_name in NON_SEARCH_FILENAMES
        ],
    }


@pytest.fixture()
async def driver() -> AsyncGenerator[DriverClient, None]:
    """Create a driver client for testing."""
    driver = DriverClient()
    await driver.initialize()
    return driver


async def test_initialize_driver(driver: DriverClient) -> None:
    """Test the initialization of the driver."""
    assert isinstance(driver.browser, Browser)


async def test_get_html(
    driver: DriverClient,
    htmls: list[str],
    urls: list[str],
) -> None:
    """Test the get_html method of the driver."""
    all_htmls = htmls["SEARCH_HTML"] + htmls["NON_SEARCH_HTML"]
    all_urls = urls["SEARCH_URLS"] + urls["NON_SEARCH_URLS"]
    for true_html, url in zip(all_htmls, all_urls, strict=True):
        fetched_html = await driver.get_html(url, wait_to_load=1)
        assert fetched_html[:300] == true_html[:300]


async def test_parse_google_search(
    driver: DriverClient,
    htmls: list[str],
) -> None:
    """Test the search_google method of the driver."""
    for html in htmls["SEARCH_HTML"]:
        results = driver._parse_google_search(html)
        for result in results:
            assert isinstance(
                result,
                SearchResult,
            ), "Result is not a SearchResult object"
            assert result.url, "Result does not have a URL"
            assert result.title, "Result does not have a title"
            assert result.description, "Result does not have a description"
    for html in htmls["NON_SEARCH_HTML"]:
        with pytest.raises(AttributeError):
            driver._parse_google_search(html)


async def test_search_google(driver: DriverClient, urls: list[str]) -> None:
    """Test the search_google method of the driver."""
    for url in urls["SEARCH_URLS"]:
        results = await driver.search_google(
            "test",
            wait_to_load=1,
            search_query_format=url,
        )
        for result in results:
            assert isinstance(
                result,
                SearchResult,
            ), "Result is not a SearchResult object"
            assert result.url, "Result does not have a URL"
            assert result.title, "Result does not have a title"
            assert result.description, "Result does not have a description"
    for url in urls["NON_SEARCH_URLS"]:
        with pytest.raises(AttributeError):
            await driver.search_google(
                "test",
                wait_to_load=1,
                search_query_format=url,
            )
