from pydantic import BaseModel, Field, HttpUrl

# Scrape API


class ScrapeRequest(BaseModel):
    """Scrape request model."""

    url: HttpUrl
    wait_to_load: int | None = Field(None, ge=0, le=300)


class ScrapeResponse(BaseModel):
    """Scrape response model."""

    url: HttpUrl
    html: str


# Search API


class SearchResult(BaseModel):
    """Model for search result entity."""

    url: str
    title: str
    description: str


class SearchRequest(BaseModel):
    """Search request model."""

    query: str
    wait_to_load: int | None = Field(None, ge=0, le=300)
