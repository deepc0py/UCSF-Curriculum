"""
Core web crawling functionality.

Handles HTTP requests, HTML parsing, and link extraction.
This is the foundation layer — no AI, just disciplined fetching and parsing.

You will build this in Meeting 1.
"""

import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field


@dataclass
class Page:
    """
    Represents a single crawled web page.

    Attributes:
        url:         The final URL after any redirects.
        status_code: HTTP status code (200, 404, etc.).
        title:       The <title> text, stripped of whitespace.
        text:        Visible page text with scripts/styles removed.
        links:       Same-domain URLs discovered on this page.
        html:        The raw HTML response body.
    """

    url: str
    status_code: int
    title: str
    text: str
    links: list[str] = field(default_factory=list)
    html: str = ""


class BasicCrawler:
    """
    An async web crawler.

    Fetches pages over HTTP, parses HTML with BeautifulSoup,
    extracts visible text and same-domain links. Respects rate
    limits and tracks visited URLs to avoid duplicate work.

    Usage:
        crawler = BasicCrawler(max_pages=10, delay=1.0)
        pages = await crawler.crawl("https://www.law.cornell.edu/uscode/text/8/1182")
    """

    def __init__(
        self,
        max_pages: int = 50,
        delay: float = 1.0,
        timeout: float = 15.0,
    ):
        self.max_pages = max_pages
        self.delay = delay
        self.timeout = timeout
        self.visited: set[str] = set()
        self.pages: list[Page] = []

    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Normalize a URL for deduplication.

        Strip the fragment (#section) and trailing slashes so that
        "https://site.com/page#top" and "https://site.com/page"
        are treated as the same URL.
        """
        raise NotImplementedError("Meeting 1")

    async def fetch_page(self, url: str) -> Page | None:
        """
        Fetch a single URL and return a parsed Page.

        Steps:
            1. Normalize the URL.
            2. Make an async GET request with httpx.
               - Set follow_redirects=True.
               - Use a descriptive User-Agent header.
            3. Check that the Content-Type is text/html.
            4. Parse the response with _parse() and return the Page.
            5. Return None if the request fails for any reason.

        Returns:
            A Page object on success, or None on failure.
        """
        raise NotImplementedError("Meeting 1")

    def _parse(self, url: str, status_code: int, html: str) -> Page:
        """
        Parse raw HTML into a structured Page object.

        Steps:
            1. Create a BeautifulSoup instance from the HTML.
            2. Remove non-content elements: script, style, nav,
               footer, header, aside.
            3. Extract the <title> text.
            4. Extract all visible text via get_text().
               Collapse blank lines.
            5. Find all <a href="..."> links on the same domain.
               Normalize each and deduplicate.
            6. Return a Page with all fields populated.
        """
        raise NotImplementedError("Meeting 1")

    async def crawl(self, start_url: str) -> list[Page]:
        """
        Breadth-first crawl starting from start_url.

        Algorithm:
            1. Initialize a queue with [start_url].
            2. While the queue is not empty and len(visited) < max_pages:
               a. Pop the next URL from the front of the queue.
               b. Skip if already visited.
               c. Mark as visited, fetch the page.
               d. If successful, add the page's links to the queue.
               e. Sleep for self.delay seconds (rate limiting).
            3. Return all successfully crawled pages.

        Returns:
            List of Page objects.
        """
        raise NotImplementedError("Meeting 1")
