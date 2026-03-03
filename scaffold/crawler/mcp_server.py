"""
MCP (Model Context Protocol) server for the web crawler.

Exposes the crawler as tools that any MCP client can use —
Claude Desktop, Claude Code, or any other MCP-compatible application.

You will build this in Meeting 4.

Run directly:
    python -m crawler.mcp_server

Or configure in Claude Desktop's settings:
    {
      "mcpServers": {
        "immigration-law-crawler": {
          "command": "python",
          "args": ["-m", "crawler.mcp_server"],
          "cwd": "/path/to/your/project"
        }
      }
    }

Key concept: MCP is a standard protocol that lets AI applications
discover and use external tools. By wrapping your crawler in an MCP
server, any MCP client can use it — without knowing anything about
your implementation. Think of it as a USB-C port for AI tools.
"""

import json
import asyncio
from mcp.server.fastmcp import FastMCP

from .core import BasicCrawler
from .rag import CrawlerRAG
from .extractor import LLMExtractor

# ── Server setup ─────────────────────────────────────────────────────────

mcp = FastMCP("immigration-law-crawler")

# TODO: Initialize shared state (CrawlerRAG, BasicCrawler instances)
#       that persists across tool calls within a session.


# ── Tools ────────────────────────────────────────────────────────────────
#
# Use the @mcp.tool() decorator to expose functions as MCP tools.
# The function's docstring becomes the tool description that clients see.
# Type hints on parameters become the input schema automatically.
#
# You need at minimum:
#   1. crawl_page         — Fetch a URL, optionally extract with LLM
#   2. search_crawled_content — Semantic search over stored findings
#   3. research_topic     — Autonomous multi-page research (uses AgentCrawler)
#
# Example:
#
#   @mcp.tool()
#   async def crawl_page(url: str, query: str = "") -> str:
#       """Crawl a legal source page and extract relevant provisions.
#
#       Args:
#           url: The URL to crawl.
#           query: Optional legal question to focus extraction on.
#       """
#       raise NotImplementedError("Meeting 4")


# ── Resources ────────────────────────────────────────────────────────────
#
# Use @mcp.resource("protocol://path") to expose read-only data.
#
# Example:
#
#   @mcp.resource("crawler://stats")
#   def get_crawler_stats() -> str:
#       """Statistics about the crawler's knowledge base."""
#       raise NotImplementedError("Meeting 4")


# ── Entry point ──────────────────────────────────────────────────────────

def main():
    mcp.run()


if __name__ == "__main__":
    main()
