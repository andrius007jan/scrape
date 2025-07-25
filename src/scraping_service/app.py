import asyncio
import logging
import os
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI

from scraping_service.helpers.error_handling import handle_errors
from scraping_service.helpers.lifespan import lifespan
from scraping_service.helpers.schemas import (
    ScrapeRequest,
    ScrapeResponse,
    SearchRequest,
    SearchResult,
)

LOGGER = logging.getLogger(__name__)
CONCURRENCY_LIMIT = int(os.getenv("CONCURRENCY_LIMIT", "5"))

app = FastAPI(lifespan=lifespan)
request_semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)


async def get_semaphore() -> AsyncGenerator[None, None]:
    """Get the semaphore to limit the number of concurrent requests."""
    async with request_semaphore:
        yield


@app.get(
    "/scrape",
    response_model=ScrapeResponse,
    dependencies=[Depends(get_semaphore)],
)
@handle_errors
async def scrape(request: ScrapeRequest) -> ScrapeResponse:
    """Scrape the given URL and return the HTML content."""
    html = await app.driver_client.get_html(str(request.url), request.wait_to_load)
    return ScrapeResponse(url=request.url, html=html)


@app.get(
    "/search",
    response_model=list[SearchResult],
    dependencies=[Depends(get_semaphore)],
)
@handle_errors
async def search(request: SearchRequest) -> list[SearchResult]:
    """Search the given query on Google and return the search results."""
    return await app.driver_client.search_google(request.query, request.wait_to_load)


@app.get("/health", response_model=dict[str, str])
async def health_check() -> dict[str, str]:
    """Health check endpoint to determine if the service is running."""
    return {"STATUS": "OK", "MESSAGE": "Service is running."}
