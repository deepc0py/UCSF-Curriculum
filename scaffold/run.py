"""
Entry point for the immigration law research agent.

Usage:
    python run.py <start_url> "<query>"

Examples:
    python run.py https://www.law.cornell.edu/uscode/text/8/chapter-12 "What are the requirements for naturalization?"
    python run.py https://www.uscis.gov/policy-manual/volume-7 "What is the process for adjusting immigration status?"

You will complete this in Meeting 5, once all other modules are built.
"""

import sys
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()


def main():
    # ── Step 1: Verify credentials ──────────────────────────────────────
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        print("Copy .env.example to .env and add your key.")
        sys.exit(1)

    # ── Step 2: Parse command-line arguments ─────────────────────────────
    if len(sys.argv) < 3:
        print('Usage: python run.py <start_url> "<query>"')
        print()
        print("Examples:")
        print('  python run.py https://www.law.cornell.edu/uscode/text/8/chapter-12 "What are the requirements for naturalization?"')
        sys.exit(1)

    start_url = sys.argv[1]
    query = " ".join(sys.argv[2:])

    # ── Step 3: Run the agent ────────────────────────────────────────────
    # TODO: Meeting 5
    #   1. Import AgentCrawler
    #   2. Create an instance with reasonable defaults
    #   3. Call agent.crawl(start_url, query) via asyncio.run()
    #   4. Print the report, pages crawled, and stats

    print("Agent not yet implemented. Complete Meetings 1–5 first.")
    sys.exit(1)


if __name__ == "__main__":
    main()
