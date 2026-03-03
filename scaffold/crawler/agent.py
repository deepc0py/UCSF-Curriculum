"""
Agent-powered web crawler.

This is the capstone module. It wires together every component —
HTTP crawling, LLM extraction, tool calling, RAG — into an autonomous
research agent that decides its own crawling strategy.

You will build this in Meeting 5 (but it depends on Meetings 1–4).

Architecture:
    ┌──────────────────────────────────────────────┐
    │               AGENT LOOP                     │
    │                                              │
    │  1. Send messages + tools to Claude           │
    │  2. Claude responds with tool_use or text     │
    │  3. If tool_use: execute tool, append result  │
    │  4. If text or "finish": we're done           │
    │  5. Go to 1                                   │
    │                                              │
    │  Components used:                             │
    │    - BasicCrawler  (core.py)    → HTTP layer  │
    │    - LLMExtractor  (extractor.py) → AI parse  │
    │    - TOOLS         (tools.py)   → tool schemas │
    │    - CrawlerRAG    (rag.py)     → memory      │
    └──────────────────────────────────────────────┘
"""

import json
import anthropic

from .core import BasicCrawler, Page
from .tools import TOOLS, format_page_for_context
from .rag import CrawlerRAG
from .extractor import LLMExtractor


SYSTEM_PROMPT = """\
You are an intelligent legal research agent specializing in US and California
immigration law. Your job is to crawl government legal sources strategically
to find statutes, regulations, and policy guidance relevant to the user's query.

Available tools:
- crawl_url: Fetch and read a web page (start here)
- extract_content: AI-powered structured extraction from a crawled page
- store_finding: Save important findings to your knowledge base
- search_findings: Semantic search over your stored findings
- finish: Complete research with a thorough final summary

Strategy:
1. Crawl the starting URL first.
2. Read the content carefully for relevant legal provisions.
3. Store important findings — include statute/regulation numbers when present.
4. Follow links to related sections, definitions, or cross-references.
5. Use search_findings to review what you've already learned.
6. When you have enough information, call finish with a comprehensive summary.

Be precise with legal citations. Note section numbers, effective dates, and
any amendments when you encounter them. Prioritize primary legal sources
(statutes and regulations) over secondary commentary.
Do not re-crawl pages you have already visited.\
"""


class AgentCrawler:
    """
    An autonomous web research agent.

    Uses Claude with tool calling to intelligently crawl the web,
    extract information, store findings in a vector database,
    and produce a research report.

    Usage:
        agent = AgentCrawler(max_steps=15, max_pages=10)
        result = await agent.crawl(
            "https://www.law.cornell.edu/uscode/text/8/1182",
            "What are the grounds for inadmissibility?"
        )
        print(result["report"])
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        max_steps: int = 20,
        max_pages: int = 50,
        delay: float = 1.0,
    ):
        self.client = anthropic.AsyncAnthropic()
        self.model = model
        self.max_steps = max_steps
        self.crawler = BasicCrawler(max_pages=max_pages, delay=delay)
        self.rag = CrawlerRAG()
        self.extractor = LLMExtractor(model=model)
        self.pages_crawled: dict[str, Page] = {}

    async def _execute_tool(self, name: str, tool_input: dict) -> str:
        """
        Route a tool call to the appropriate handler.

        This is the bridge between Claude's tool_use requests and your
        actual Python code. Map each tool name to its implementation:

            "crawl_url"        → self.crawler.fetch_page()
            "extract_content"  → self.extractor.extract()
            "store_finding"    → self.rag.store()
            "search_findings"  → self.rag.search()
            "finish"           → return completion status

        Return results as JSON strings — that's what goes back to Claude
        as a tool_result.

        Don't forget:
            - Track crawled pages in self.pages_crawled
            - Handle "already crawled" gracefully
            - Handle "page not found" gracefully
        """
        raise NotImplementedError("Meeting 5")

    async def crawl(self, start_url: str, query: str) -> dict:
        """
        Run the agent crawler.

        This is the agent loop — the core pattern from Meeting 3,
        now with all components wired together.

        Algorithm:
            1. Build the initial messages list with the user's query.
            2. For each step (up to max_steps):
               a. Call client.messages.create() with SYSTEM_PROMPT,
                  TOOLS, and messages.
               b. Append the assistant's response to messages.
               c. If stop_reason == "end_turn": extract text, break.
               d. If stop_reason == "tool_use":
                  - For each tool_use block, call _execute_tool().
                  - Build tool_result messages and append.
                  - If "finish" was called, capture the summary and break.
            3. If the loop exhausted max_steps without finishing,
               send one final message (without tools) asking for a summary.
            4. Return a dict with:
               - report: the final summary text
               - pages_crawled: list of URLs visited
               - findings_stored: count from RAG
               - steps_taken: number of loop iterations

        Args:
            start_url: The URL to begin research from.
            query:     The research question to investigate.

        Returns:
            Dict with report, pages_crawled, findings_stored, steps_taken.
        """
        raise NotImplementedError("Meeting 5")
