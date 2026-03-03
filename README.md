# UCSF-Curriculum

An AI-powered immigration law research crawler, built from scratch over a
10-week quarter. This is the course repository for a hands-on curriculum
that teaches modern CS concepts — agents, prompting, context windows, RAG,
tool calling, and Model Context Protocol — through the lens of a real
application: navigating US and California immigration law.

## What This Is

A structured curriculum for 3 students meeting biweekly (5 meetings, 2 hours
each) with homework periods in between. Students start with an empty scaffold
and progressively implement a system that can:

- Crawl federal and state legal sources (Cornell LII, eCFR, USCIS)
- Extract structured data from statutory text using an LLM
- Make autonomous crawling decisions via tool calling
- Build a searchable knowledge base with vector embeddings (RAG)
- Expose the crawler as a service via Model Context Protocol (MCP)

By the end, the scaffold becomes a working legal research agent.

## Repository Structure

```
├── curriculum/                    Course materials (released on a rolling schedule)
│   ├── README.md                  Course overview, setup, and schedule
│   └── meeting-1-foundations.md   Meeting 1: HTTP, HTML parsing, intro to LLMs
│                                  Meetings 2–5 released before each session
│
└── scaffold/                      Student starter code
    ├── run.py                     Entry point (stubbed)
    ├── requirements.txt           Python dependencies
    ├── .env.example               API key template
    └── crawler/
        ├── __init__.py            Module index
        ├── core.py                HTTP crawling and HTML parsing      (Meeting 1)
        ├── extractor.py           LLM-powered content extraction      (Meeting 2)
        ├── tools.py               Tool schemas for Claude             (Meeting 3)
        ├── rag.py                 ChromaDB vector store               (Meeting 4)
        ├── mcp_server.py          MCP server                         (Meeting 4)
        └── agent.py               Autonomous research agent           (Meeting 5)
```

Every scaffold file has full type hints, comprehensive docstrings, and
`raise NotImplementedError("Meeting N")` stubs indicating which session
covers the implementation.

## Schedule

| Meeting | Week | Topic | What Students Build |
|---------|------|-------|---------------------|
| 1 | 1 | The Web as Data | `core.py` — async crawler with BeautifulSoup |
| 2 | 3 | Teaching Machines to Read | `extractor.py` — LLM extraction pipeline |
| 3 | 5 | Giving AI Hands | `tools.py` — tool calling and the agent loop |
| 4 | 7 | Memory and Protocol | `rag.py` + `mcp_server.py` — RAG and MCP |
| 5 | 9 | The Complete Agent | `agent.py` + `run.py` — full integration |

## Getting Started

Students should follow the setup instructions in
[`curriculum/README.md`](curriculum/README.md), which covers:

1. Python 3.11+ virtual environment
2. Installing dependencies (`pip install -r scaffold/requirements.txt`)
3. Getting an Anthropic API key
4. Verifying the environment

## Legal Sources Used

| Source | What It Contains |
|--------|-----------------|
| [Cornell LII — Title 8](https://www.law.cornell.edu/uscode/text/8) | Immigration and Nationality Act (federal statute) |
| [eCFR — Title 8](https://www.ecfr.gov/current/title-8) | Federal immigration regulations |
| [USCIS Policy Manual](https://www.uscis.gov/policy-manual) | Official USCIS guidance and procedures |
| [CA Legislature](https://leginfo.legislature.ca.gov) | California state statutes |

All sources are public domain or freely available government publications
(17 USC § 105; CA Gov. Code § 6254).

## Topics Covered

These are the concepts current CS textbooks don't teach but the industry
now expects:

- **Prompting** — instructing LLMs effectively for data extraction
- **Context windows** — token budgets, truncation, and chunking strategies
- **Tool calling** — letting models invoke functions autonomously
- **Agent loops** — the observe-think-act pattern behind every AI agent
- **RAG** — retrieval-augmented generation with vector embeddings
- **MCP** — the Model Context Protocol for standardized AI tool interop

## License

Curriculum materials and scaffold code are provided for educational use.
