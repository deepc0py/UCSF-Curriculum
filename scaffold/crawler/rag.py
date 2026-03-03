"""
RAG (Retrieval-Augmented Generation) component.

Stores crawled content as vector embeddings in ChromaDB so the agent
can semantically search its own findings — giving it persistent memory
across a crawling session.

You will build this in Meeting 4.

Key concept: Instead of keeping every crawled page in the conversation
history (which fills the context window and gets expensive), we store
findings externally and retrieve only what's relevant to the current
step. That's the "retrieval" in Retrieval-Augmented Generation.
"""

import uuid
import chromadb


class CrawlerRAG:
    """
    Vector store for crawler findings using ChromaDB.

    ChromaDB handles embedding (converting text to vectors) and
    similarity search automatically. You just call add() and query().

    Usage:
        rag = CrawlerRAG()
        rag.store("INA § 212(a)(2) covers criminal grounds...", "https://...", ["criminal"])
        results = rag.search("What are the criminal inadmissibility grounds?")
    """

    def __init__(
        self,
        collection_name: str = "crawler_findings",
        persist_dir: str | None = None,
    ):
        """
        Initialize the vector store.

        Args:
            collection_name: Name for the ChromaDB collection.
            persist_dir:     If provided, store data on disk at this path.
                             If None, use an in-memory database (lost on exit).

        Setup:
            - Create a chromadb.Client() or PersistentClient()
            - Call get_or_create_collection() with cosine distance metric
        """
        raise NotImplementedError("Meeting 4")

    def store(
        self,
        content: str,
        source_url: str,
        tags: list[str] | None = None,
    ) -> str:
        """
        Store a finding as a vector embedding.

        Steps:
            1. Generate a unique document ID (uuid4).
            2. Build a metadata dict with source_url and optional tags.
            3. Call self.collection.add() with the document, metadata, and ID.

        Args:
            content:    The text to store and make searchable.
            source_url: Where this content came from.
            tags:       Optional categorization tags.

        Returns:
            The generated document ID.
        """
        raise NotImplementedError("Meeting 4")

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        """
        Semantic similarity search over stored findings.

        Steps:
            1. Return [] if the collection is empty.
            2. Cap n_results at the collection size.
            3. Call self.collection.query() with the query text.
            4. Transform the results into a list of dicts, each with:
               content, source_url, tags, distance.

        Args:
            query:     Natural-language search query.
            n_results: Max results to return.

        Returns:
            List of dicts with content, source_url, tags, distance.
        """
        raise NotImplementedError("Meeting 4")

    def count(self) -> int:
        """Return the number of stored findings."""
        raise NotImplementedError("Meeting 4")
