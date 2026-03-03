# Building an AI-Powered Legal Research Crawler: A 10-Week Curriculum

## Overview

This curriculum teaches modern web scraping through the lens of AI-powered
agents, applied to a real problem: navigating US and California immigration
law. Over 5 meetings (10 weeks), you will build a web crawler that evolves
from a simple HTTP scraper into an autonomous legal research agent powered
by large language models.

Immigration law is scattered across federal statutes (Title 8 USC), federal
regulations (8 CFR), USCIS policy manuals, California state codes, and
government agency pages. No single search engine unifies them. You're going
to build something that does.

By the end, you will have built and understood every layer of a system that can:
- Crawl government legal sources and extract structured data
- Use an LLM to intelligently parse statutory and regulatory language
- Make autonomous decisions about which legal provisions to follow (tool calling)
- Remember what it has learned across dozens of pages (RAG)
- Expose itself as a legal research service via Model Context Protocol (MCP)

**A note on data:** US federal statutes, regulations, and government agency
publications are public domain. California legislative texts are freely
available under Government Code § 6254. You are not scraping copyrighted
material — you are indexing the law itself.

## Schedule

| Meeting | Week | Topic | Key Concepts |
|---------|------|-------|--------------|
| 1 | 1 | [The Web as Data](meeting-1-foundations.md) | HTTP, HTML parsing, basic scraping, intro to LLMs |
| 2 | 3 | [Teaching Machines to Read](meeting-2-llm-extraction.md) | Context windows, prompt engineering, structured extraction |
| 3 | 5 | [Giving AI Hands](meeting-3-tool-calling.md) | Tool calling, agent loops, autonomous decision-making |
| 4 | 7 | [Memory and Protocol](meeting-4-rag-and-mcp.md) | Vector embeddings, RAG, Model Context Protocol |
| 5 | 9 | [The Complete Agent](meeting-5-agent-workflows.md) | Agent workflows, integration, architecture review |

Each meeting is 2 hours. You have a 2-week break between meetings to complete
homework and experiment.

## Setup (Do This Before Meeting 1)

### 1. Python environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install httpx beautifulsoup4 anthropic chromadb "mcp[cli]" python-dotenv
```

### 2. Get an Anthropic API key

- Go to https://console.anthropic.com
- Create an account and generate an API key
- Create a `.env` file in your project root:
  ```
  ANTHROPIC_API_KEY=sk-ant-your-key-here
  ```

### 3. Verify everything works

```python
import httpx, bs4, anthropic, chromadb
print("All imports successful")
```

## Philosophy

This curriculum assumes you already know how to program. You are CS students.
What you may not know — and what current textbooks largely don't cover — is
how to build systems where AI models are active participants rather than passive
tools. The concepts here (agents, tool calling, RAG, MCP) are not academic
curiosities. They are the primitives of a new generation of software.

We learn them by building something real — a tool that could genuinely help
immigration attorneys, legal aid organizations, and policy researchers
navigate one of the most complex areas of US law.

## Key Legal Sources

| Source | URL | What It Contains |
|--------|-----|-----------------|
| Cornell LII — Title 8 | law.cornell.edu/uscode/text/8 | Immigration and Nationality Act (federal statute) |
| eCFR — Title 8 | ecfr.gov/current/title-8 | Federal immigration regulations |
| USCIS Policy Manual | uscis.gov/policy-manual | Official USCIS guidance and procedures |
| CA Legislature | leginfo.legislature.ca.gov | California state statutes (incl. immigrant protections) |

All of these are public domain or freely available government publications.

## Project Structure

```
crawler/
├── core.py          # Meeting 1-2: HTTP crawling and HTML parsing
├── extractor.py     # Meeting 2-3: LLM-powered content extraction
├── tools.py         # Meeting 3:   Tool definitions for the agent
├── rag.py           # Meeting 4:   Vector store for persistent memory
├── mcp_server.py    # Meeting 4:   MCP server exposing the crawler
├── agent.py         # Meeting 5:   Full agent loop tying it all together
run.py               # Entry point
```

Each file corresponds to concepts introduced in specific meetings. By Meeting 5,
you will understand every line of every file.
