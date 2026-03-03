"""
Tool definitions for the agent crawler.

These tool schemas are passed to Claude's tool-use API. The model reads
them to understand what actions it can take, then responds with tool_use
blocks requesting specific function calls.

You will build this in Meeting 3.

Hint: Each tool is a dict with three keys:
    - "name":         A short identifier (e.g., "crawl_url")
    - "description":  What the tool does — the model reads this to decide
                      when to use it. Write it like you're explaining the
                      tool to a colleague.
    - "input_schema": A JSON Schema object defining the parameters.
"""

from .core import Page


# ── Tool schemas ─────────────────────────────────────────────────────────
#
# Define a list of tool dicts. You need at minimum:
#
#   1. crawl_url       — Fetch and read a web page.
#   2. extract_content — AI extraction from a previously crawled page.
#   3. store_finding   — Save a finding to the knowledge base.
#   4. search_findings — Semantic search over stored findings.
#   5. finish          — End the session with a final summary.
#
# Each tool's input_schema should specify required and optional params
# with clear descriptions. The better your descriptions, the better
# the model will use your tools.

TOOLS: list[dict] = [
    # TODO: Meeting 3 — define your tool schemas here.
    #
    # Example structure for one tool:
    # {
    #     "name": "crawl_url",
    #     "description": "Fetch and read a web page. Returns ...",
    #     "input_schema": {
    #         "type": "object",
    #         "properties": {
    #             "url": {
    #                 "type": "string",
    #                 "description": "The full URL to crawl",
    #             }
    #         },
    #         "required": ["url"],
    #     },
    # },
]


def format_page_for_context(page: Page, max_chars: int = 8000) -> str:
    """
    Format a Page into a string suitable for the agent's context window.

    The agent sees this string as the result of a crawl_url tool call.
    Include:
        - The URL, title, and status code
        - The page text (truncated to max_chars)
        - A list of discovered links (cap at ~20)

    Keep it information-dense but within budget. Every character here
    costs tokens on the next API call.

    Args:
        page:      The Page object to format.
        max_chars: Maximum characters for the text portion.

    Returns:
        A formatted string.
    """
    raise NotImplementedError("Meeting 3")
