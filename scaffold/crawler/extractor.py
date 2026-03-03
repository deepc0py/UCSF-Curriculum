"""
LLM-powered content extraction.

Uses Claude to intelligently extract structured data from raw web pages.
This is where unstructured legal text becomes structured knowledge.

You will build this in Meeting 2.
"""

import json
import anthropic
from .core import Page


class LLMExtractor:
    """
    Uses Claude to extract structured information from crawled pages.

    The extractor sends page text to the Anthropic Messages API with
    a carefully engineered prompt, and parses the JSON response into
    a Python dict.

    Usage:
        extractor = LLMExtractor()
        result = await extractor.extract(page, focus="inadmissibility grounds")
        # result = {"title": "...", "summary": "...", "key_facts": [...], ...}
    """

    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.AsyncAnthropic()
        self.model = model

    @staticmethod
    def _truncate(text: str, max_chars: int = 12_000) -> str:
        """
        Truncate text to stay within a reasonable context budget.

        12,000 characters is roughly 3,000 tokens — leaving room for
        the prompt template and the model's response within the context
        window.

        If the text is already short enough, return it unchanged.
        Otherwise, cut at max_chars and append a truncation notice.
        """
        raise NotImplementedError("Meeting 2")

    async def extract(self, page: Page, focus: str = "") -> dict:
        """
        Extract structured information from a page using Claude.

        Build a prompt that includes:
            - The page URL and title
            - The page text (truncated if needed)
            - An optional focus area
            - Instructions to respond with JSON containing:
              title, summary, key_facts, topics, relevance

        Parse the model's response as JSON. Handle edge cases:
            - Model may wrap JSON in ```json ... ``` fences
            - Model may return invalid JSON (return a fallback dict)

        Args:
            page:  A crawled Page object.
            focus: Optional string to narrow the extraction.

        Returns:
            Dict with title, summary, key_facts, topics, relevance.
        """
        raise NotImplementedError("Meeting 2")

    async def summarize_findings(
        self, findings: list[dict], query: str
    ) -> str:
        """
        Synthesize multiple extraction results into a final report.

        Build a prompt that presents all findings and asks the model
        to produce a comprehensive summary answering the original query.

        Args:
            findings: List of dicts from extract().
            query:    The original research query.

        Returns:
            A prose summary string.
        """
        raise NotImplementedError("Meeting 2")
