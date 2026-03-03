# Meeting 1: The Web as Data

**Week 1 — 2 hours**

## Pre-Meeting Preparation

- Install Python 3.11+
- Set up your virtual environment (see README)
- Get an Anthropic API key
- Skim: [MDN — HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

## Learning Objectives

By the end of this meeting you will be able to:
1. Explain the HTTP request/response cycle
2. Fetch web pages programmatically with Python
3. Parse HTML and extract text and links using BeautifulSoup
4. Describe what a large language model is and what "prompting" means
5. Make your first API call to Claude

---

## Part 1: How the Web Works (30 min)

### HTTP in 5 Minutes

Every web page you've ever seen was delivered by the same mechanism:

```
Client (your code)                     Server (website)
       |                                     |
       |  --- GET /page HTTP/1.1 ----------> |
       |                                     |
       |  <-- 200 OK + HTML body ----------  |
```

Your browser hides this from you. Your crawler will not.

Key things to know:
- **Methods**: GET (read), POST (submit). For crawling, you only need GET.
- **Status codes**: 200 (ok), 301/302 (redirect), 403 (forbidden), 404 (gone), 429 (rate limited)
- **Headers**: `User-Agent` identifies your client. `Content-Type` tells you what you received.
- **robots.txt**: A file at `/robots.txt` that says what crawlers are and aren't welcome to access. Respect it.

### HTML: The Document Tree

HTML is a tree of nested elements. A simplified page:

```html
<html>
  <head><title>My Page</title></head>
  <body>
    <h1>Welcome</h1>
    <p>Some content with a <a href="/other">link</a>.</p>
  </body>
</html>
```

Parsing HTML means navigating this tree to find the data you want. The
tool for this in Python is **BeautifulSoup**.

### Ethics and Legality of Scraping

Before you scrape anything:
1. Check `robots.txt`
2. Rate-limit your requests (1 request/second is a good default)
3. Identify yourself with a descriptive User-Agent
4. Don't scrape data behind authentication unless you have explicit permission
5. Store only what you need

**Good news for us:** US federal statutes, regulations, and government
agency publications are public domain — they cannot be copyrighted (17
USC § 105). California legislative texts are freely available under
Government Code § 6254. We are building a tool to index *the law itself*.
The ethical and legal footing could not be cleaner.

---

## Part 2: Hands-On — Building a Basic Crawler (45 min)

### Step 1: Fetching a page

Let's start with the Immigration and Nationality Act on Cornell's Legal
Information Institute — one of the best freely accessible legal sources:

```python
import httpx

url = "https://www.law.cornell.edu/uscode/text/8/chapter-12"

response = httpx.get(url, follow_redirects=True)
print(f"Status: {response.status_code}")
print(f"Content type: {response.headers['content-type']}")
print(f"Body length: {len(response.text)} chars")
```

### Step 2: Parsing with BeautifulSoup

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")

# Get the page title
print(f"Title: {soup.title.string}")

# Find section headings — these are the statutory sections
for heading in soup.find_all(["h2", "h3"]):
    print(heading.get_text(strip=True))
```

### Step 3: Extracting links

```python
from urllib.parse import urljoin

links = []
for a in soup.find_all("a", href=True):
    full_url = urljoin(url, a["href"])
    links.append(full_url)
    print(full_url)
```

`urljoin` is critical — it resolves relative URLs (`/section-1101`) against
the base URL to produce absolute URLs
(`https://www.law.cornell.edu/uscode/text/8/section-1101`).

### Step 4: A multi-page crawler

```python
import httpx
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

async def crawl(start_url, max_pages=5):
    visited = set()
    queue = [start_url]

    async with httpx.AsyncClient() as client:
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited:
                continue

            visited.add(url)
            print(f"[{len(visited)}] {url}")

            try:
                resp = await client.get(url, follow_redirects=True)
                soup = BeautifulSoup(resp.text, "html.parser")

                # Extract text
                title = soup.title.string if soup.title else "No title"
                text = soup.get_text(separator=" ", strip=True)[:200]
                print(f"    Title: {title}")
                print(f"    Preview: {text}...")

                # Find same-domain links
                base_domain = urlparse(start_url).netloc
                for a in soup.find_all("a", href=True):
                    link = urljoin(url, a["href"])
                    if urlparse(link).netloc == base_domain:
                        queue.append(link)

                await asyncio.sleep(1)  # Rate limit
            except Exception as e:
                print(f"    Error: {e}")

asyncio.run(crawl("https://www.law.cornell.edu/uscode/text/8/chapter-12"))
```

This is the core of every web crawler. Everything we build from here
adds intelligence on top of this loop. Notice how even 5 pages into
Title 8 gives you a sense of how immigration law is organized —
definitions in § 1101, admission categories, naturalization requirements,
deportation grounds — all connected by cross-references.

### Step 5: Your first LLM call

```python
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY from environment

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "What is 8 USC § 1101(a)(15)? Explain in 2 sentences."}
    ]
)

print(message.content[0].text)
```

That's it. You've just prompted a large language model. The `messages` list
is the conversation. The model reads it and generates a response. The
`max_tokens` parameter caps how long the response can be.

We'll use this exact API to make our crawler intelligent — imagine pointing
it at a section of the INA and having it explain the legal provisions in
plain language, or extract the eligibility requirements as structured data.

---

## Part 3: Discussion (15 min)

Questions to consider:
- What happens when a page loads content dynamically with JavaScript? (Our scraper won't see it — we'll address this.)
- How is talking to an LLM API different from calling a regular function?
- What makes a web page "easy" or "hard" to scrape?
- Why is immigration law particularly well-suited for this kind of tool?
  (Scattered across agencies, dense cross-references, public domain text)

---

## Homework (Due Meeting 2, Week 3)

### Assignment: Build an immigration law scraper

Pick ONE of these legal sources:
- **Cornell LII**: `https://www.law.cornell.edu/uscode/text/8/chapter-12`
  (Immigration and Nationality Act)
- **USCIS Policy Manual**: `https://www.uscis.gov/policy-manual`
- **eCFR Title 8**: `https://www.ecfr.gov/current/title-8`

Build a Python script that:

1. **Crawls** at least 10 pages on that site, staying on the same domain
2. **Extracts** the title and main text content from each page
3. **Stores** the results in a JSON file with this structure:
   ```json
   [
     {
       "url": "https://www.law.cornell.edu/uscode/text/8/1101",
       "title": "8 USC § 1101 - Definitions",
       "text": "The main content...",
       "links_found": 15
     }
   ]
   ```
4. **Respects** robots.txt and uses a 1-second delay between requests

### Stretch goal

Make a second script that sends the extracted text from one of your
scraped legal pages to Claude and asks it to summarize the section in
3 bullet points in plain English. Think about: statutory text is dense
— what happens if the section is very long?

### Reading for next time

- [Anthropic: Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Anthropic: Messages API Reference](https://docs.anthropic.com/en/api/messages)
