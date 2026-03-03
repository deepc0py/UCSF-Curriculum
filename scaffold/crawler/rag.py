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
        use_reranker: bool = False,
    ):
        """
        Initialize the vector store.

        Args:
            collection_name: Name for the ChromaDB collection.
            persist_dir:     If provided, store data on disk at this path.
                             If None, use an in-memory database (lost on exit).
            use_reranker:    If True, use a cross-encoder (FlashRank) to
                             rerank search results. Two-stage retrieval:
                             1. Retrieve broadly with cosine similarity (3x candidates)
                             2. Rerank precisely with a cross-encoder (return top N)

        Setup:
            - Create a chromadb.Client() or PersistentClient()
            - Call get_or_create_collection() with cosine distance metric
            - Store use_reranker flag and initialize _ranker = None (lazy init)
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

    def _rerank(self, query: str, findings: list[dict], top_n: int) -> list[dict]:
        """
        Stretch goal: Rerank findings using a cross-encoder model (FlashRank).

        This scores each (query, document) pair jointly — much more accurate
        than comparing two embeddings independently via cosine similarity.

        Steps:
            1. Import and initialize flashrank.Ranker (lazy, via self._get_ranker())
            2. Build passage dicts: [{"id": i, "text": finding["content"]}, ...]
            3. Create a RerankRequest(query=query, passages=passages)
            4. Call ranker.rerank(request)
            5. Sort by score descending, take top_n
            6. Add "rerank_score" to each finding dict

        See: https://github.com/PrithivirajDamodaran/FlashRank
        """
        raise NotImplementedError("Meeting 4 stretch")

    def count(self) -> int:
        """Return the number of stored findings."""
        raise NotImplementedError("Meeting 4")
