"""
Immigration Law Research Crawler

An AI-powered agent that crawls government legal sources,
extracts structured data, and builds a searchable knowledge base.

Modules:
    core        — HTTP crawling and HTML parsing (Meeting 1)
    extractor   — LLM-powered content extraction (Meeting 2)
    tools       — Tool schemas for the agent (Meeting 3)
    rag         — Vector store for persistent memory (Meeting 4)
    mcp_server  — Model Context Protocol server (Meeting 4)
    agent       — Autonomous research agent (Meeting 5)
"""

from .core import BasicCrawler, Page
from .extractor import LLMExtractor
from .rag import CrawlerRAG
from .agent import AgentCrawler
