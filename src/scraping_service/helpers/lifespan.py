import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from scraping_service.helpers.driver import DriverClient

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage resources during the lifespan of the application."""
    # Set up
    LOGGER.info("Setting up timed driver.")
    app.driver_client = DriverClient()
    await app.driver_client.initialize()
    LOGGER.info("Driver setup complete.")
    yield
    # Clean up
    app.driver_client.close()
    LOGGER.info("Driver quit.")
