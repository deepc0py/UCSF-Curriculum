# Meeting 4: Memory and Protocol

**Week 7 — 2 hours**

## Pre-Meeting Preparation

- Complete Meeting 3 homework (multi-tool agent crawler)
- Read: [MCP Introduction](https://modelcontextprotocol.io/introduction)
- Read about vector embeddings conceptually (any introductory resource)
- Install ChromaDB: `pip install chromadb`

## Learning Objectives

By the end of this meeting you will be able to:
1. Explain why agents need persistent memory and what RAG solves
2. Describe how vector embeddings and similarity search work
3. Build a RAG pipeline with ChromaDB
4. Explain the Model Context Protocol and why it exists
5. Build an MCP server that exposes your crawler to any MCP client

---

## Part 1: The Memory Problem and RAG (40 min)

### Why Agents Need Memory

Your Meeting 3 agent has a fundamental limitation: it accumulates everything
in the conversation history. Every page it crawls gets appended to the
messages list. This means:

1. **Context window fills up.** After crawling 10-15 pages, you're pushing
   the token limit.
2. **Cost grows quadratically.** Each API call sends the *entire* history.
   Step 10 is 10x more expensive than step 1.
3. **No persistence.** When the script ends, everything is gone.

RAG — **Retrieval-Augmented Generation** — solves this by giving the agent
an external memory it can write to and search.

### How RAG Works

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│  Web Page   │ ───► │ Store as vector  │ ───► │ Vector DB   │
│  (text)     │      │ embedding        │      │ (ChromaDB)  │
└─────────────┘      └──────────────────┘      └─────────────┘

                     Later...

┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│  Query:     │ ───► │ Convert to       │ ───► │ Find similar │
│  "asylum    │      │ vector, search   │      │ documents   │
│   grounds"  │      │ by similarity    │      │             │
└─────────────┘      └──────────────────┘      └─────────────┘
```

The key insight: instead of storing text as text, you store it as a
**vector embedding** — a list of numbers that captures the text's *meaning*.

### Vector Embeddings in 60 Seconds

An embedding model converts text into a fixed-size array of floats:

```
"removal proceedings under section 240" → [0.12, -0.45, 0.78, ..., 0.33]  (384 dimensions)
"deportation hearings per INA § 240"   → [0.11, -0.43, 0.76, ..., 0.31]  (similar!)
"corporate merger tax implications"    → [0.89, 0.12, -0.56, ..., -0.22]  (very different)
```

Texts with similar meanings produce vectors that are close together in
high-dimensional space. You can find related documents by measuring the
**cosine distance** between vectors.

You don't need to understand the math deeply. Just know:
- Similar text → similar vectors → small distance
- Different text → different vectors → large distance
- ChromaDB handles the embedding and search for you

This is critical for legal research: the same concept is often described
with different terminology across statutes, regulations, and policy guidance.
"Removal" in one section means "deportation" in an older one. Semantic
search handles this naturally.

### Building with ChromaDB

```python
import chromadb

# Create an in-memory database
client = chromadb.Client()
collection = client.create_collection("immigration_law")

# Store some legal provisions
collection.add(
    documents=[
        "An alien is inadmissible if convicted of a crime involving moral turpitude",
        "Asylum may be granted to any alien who demonstrates persecution on account of race, religion, nationality, political opinion, or membership in a particular social group",
        "An alien who was not inspected and admitted or paroled into the US is inadmissible under section 212(a)(6)(A)",
    ],
    ids=["doc1", "doc2", "doc3"],
    metadatas=[
        {"source": "8 USC § 1182(a)(2)"},
        {"source": "8 USC § 1158(b)(1)"},
        {"source": "8 USC § 1182(a)(6)"},
    ]
)

# Search by meaning (not keywords!)
results = collection.query(
    query_texts=["What are the grounds for denying entry based on criminal history?"],
    n_results=2
)

print(results["documents"])
# → [['An alien is inadmissible if convicted of a crime involving moral turpitude',
#     'An alien who was not inspected and admitted...']]
```

Notice: the query says "denying entry" and "criminal history" but the top
result says "inadmissible" and "crime involving moral turpitude." Keyword
search would miss this. Semantic search finds it because the *meanings*
are related — exactly the kind of terminological gap that makes legal
research hard.

### Integrating RAG into the Crawler

Here's the `CrawlerRAG` class — look at how simple it is:

```python
import uuid
import chromadb

class CrawlerRAG:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="crawler_findings",
            metadata={"hnsw:space": "cosine"}
        )

    def store(self, content, source_url, tags=None):
        doc_id = str(uuid.uuid4())
        metadata = {"source_url": source_url}
        if tags:
            metadata["tags"] = ",".join(tags)
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id

    def search(self, query, n_results=5):
        if self.collection.count() == 0:
            return []
        n = min(n_results, self.collection.count())
        results = self.collection.query(query_texts=[query], n_results=n)
        return [
            {
                "content": results["documents"][0][i],
                "source_url": results["metadatas"][0][i].get("source_url"),
                "distance": results["distances"][0][i]
            }
            for i in range(len(results["documents"][0]))
        ]
```

Now add `store_finding` and `search_findings` tools to your agent from
Meeting 3, backed by this class. The agent can now:
- **Store** important findings as it crawls (persistent memory)
- **Search** its own findings before deciding what to crawl next (retrieval)

This is RAG. The agent's generation (its responses and decisions) is
augmented by retrieval from its own knowledge base.

### Limits of Cosine Similarity

Cosine similarity is fast but imprecise. It finds neighbors in vector
space, but not necessarily the *best answer* to a question. The embedding
model converts query and document independently — it never sees them
together. This means it can miss nuanced relevance, especially when the
query uses different terminology than the stored text.

A **cross-encoder** (reranker) fixes this. It takes a (query, document) pair
as a single input and scores them jointly — much more accurate, but too slow
to run against every document. The solution is **two-stage retrieval**:

1. **Retrieve broadly**: fetch 3x candidates from ChromaDB using cosine similarity
2. **Rerank precisely**: score each candidate with a cross-encoder, return the top N

This pattern is standard in production RAG systems. Here's the code using
[FlashRank](https://github.com/PrithivirajDamodaran/FlashRank), a lightweight
reranker that runs on `onnxruntime` (already installed with ChromaDB):

```python
from flashrank import Ranker, RerankRequest

ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")  # ~25MB download on first call

passages = [{"id": i, "text": doc} for i, doc in enumerate(documents)]
request = RerankRequest(query="grounds for asylum", passages=passages)
results = ranker.rerank(request)

for r in sorted(results, key=lambda x: x["score"], reverse=True):
    print(f"  Score {r['score']:.6f}: {passages[r['id']]['text'][:80]}")
```

---

## Part 2: Model Context Protocol (40 min)

### What Is MCP?

So far, your crawler is a Python script. To use it, you run it from the
command line. But what if Claude Desktop (or any AI application) could
use your crawler directly?

**Model Context Protocol (MCP)** is a standard that lets AI applications
discover and use external tools. Think of it as a USB-C port for AI:
any MCP server works with any MCP client.

```
┌──────────────┐     MCP      ┌──────────────────┐
│ Claude       │ ◄──────────► │ Your Crawler      │
│ Desktop      │   (JSON-RPC) │ (MCP Server)      │
└──────────────┘              └──────────────────┘

┌──────────────┐     MCP      ┌──────────────────┐
│ Claude Code  │ ◄──────────► │ Your Crawler      │
│ (CLI)        │              │ (same server!)    │
└──────────────┘              └──────────────────┘
```

MCP defines three primitives:
- **Tools**: Functions the AI can call (like our crawler tools)
- **Resources**: Data the AI can read (like crawler stats)
- **Prompts**: Reusable prompt templates

### Building an MCP Server

The Python MCP SDK provides `FastMCP`, which makes building servers trivial:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web-crawler")

@mcp.tool()
async def crawl_page(url: str, query: str = "") -> str:
    """Crawl a web page and optionally extract content relevant to a query.

    Args:
        url: The URL to crawl.
        query: Optional focus query for extraction.
    """
    # Your crawling code here
    page = await crawler.fetch_page(url)
    if not page:
        return f"Failed to fetch {url}"
    return f"Title: {page.title}\n\n{page.text[:3000]}"

@mcp.tool()
async def search_knowledge(query: str) -> str:
    """Search previously crawled content by semantic similarity.

    Args:
        query: Natural-language search query.
    """
    results = rag.search(query)
    return json.dumps(results, indent=2)

@mcp.resource("crawler://stats")
def get_stats() -> str:
    """Get crawler statistics."""
    return json.dumps({"findings": rag.count()})

if __name__ == "__main__":
    mcp.run()
```

Notice: the tool descriptions and type hints in the function signatures
are what MCP clients use to understand what your tools do. Write them well.

### Connecting to Claude Desktop

Create or edit the Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "web-crawler": {
      "command": "python",
      "args": ["-m", "crawler.mcp_server"],
      "cwd": "/path/to/your/project",
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Restart Claude Desktop. Your crawler tools now appear in Claude's tool
list. You can say "crawl this URL and tell me what you find" and Claude
will use your MCP server to do it.

### Why MCP Matters

MCP is to AI applications what HTTP was to web browsers. It's the
standardized protocol that lets:
- Any AI app use any tool
- Tools be built once and shared across applications
- Tool authors not worry about which AI client their users prefer

Right now (2026), the MCP ecosystem is still young but growing fast.
Building MCP servers is a high-leverage skill.

---

## Part 3: Discussion (10 min)

- How is RAG different from just putting everything in the context window?
  (Think about: cost, scale, relevance filtering)
- What other tools could you expose via MCP? (Case law search, form
  lookup, filing deadline calculator, regulatory history...)
- ChromaDB stores embeddings in memory or on disk. What would you need for
  a production legal research system? (Think: PostgreSQL + pgvector,
  Pinecone, Weaviate — plus audit trails for legal reliability)
- MCP uses JSON-RPC over stdio or SSE. Why stdio for local tools?
- How could a legal aid organization use an MCP server like this?

---

## Homework (Due Meeting 5, Week 9)

### Assignment: RAG-powered MCP crawler

Build a complete system with two components:

**Component 1: Agent crawler with RAG**
- Integrate ChromaDB into your Meeting 3 agent
- The `store_finding` tool should write to ChromaDB
- The `search_findings` tool should query ChromaDB
- After crawling, the agent should use `search_findings` to verify its
  findings before producing the final summary

**Component 2: MCP server**
- Create an MCP server with at least 3 tools:
  - `crawl_page`: Fetch and return a page's content
  - `search_knowledge`: Search the RAG database
  - One tool of your own design
- Add at least one resource (e.g., stats, recent crawls)
- Test it with Claude Desktop or `mcp dev`

### Testing your MCP server

You can test without Claude Desktop using the MCP inspector:

```bash
mcp dev crawler/mcp_server.py
```

This opens a web UI where you can call your tools directly.

### Stretch goals

**Reranking**: Add reranking to your search method using FlashRank. Retrieve 3x
candidates from ChromaDB, rerank with a cross-encoder, and return the top N.
Compare results with and without reranking on the same queries — you should see
the most relevant result rise to the top even when it uses different terminology
than your query.

**Persistent storage**: Use `chromadb.PersistentClient(path="./data")` so
findings survive between runs. Start the crawler, crawl some pages, stop it,
restart it, and search for findings from the previous session.

### Preparing for Meeting 5

- Have your full agent crawler working end-to-end
- Be ready to demo your project
- Write down: one thing that surprised you and one thing that confused you
