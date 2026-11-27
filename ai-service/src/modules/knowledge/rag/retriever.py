"""
Document retrieval for the Knowledge Agent.

The retriever coordinates embedding generation and vector
store search. It does not generate the final AI answer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from modules.knowledge.exceptions import (
    KnowledgeRetrievalError,
    NoRelevantDocumentsFound,
)
from modules.knowledge.rag.embeddings import EmbeddingProvider
from modules.knowledge.rag.vector_store import VectorStore
from modules.knowledge.schemas import RetrievedDocument


class Retriever(ABC):
    """
    Abstract interface for knowledge retrieval.
    """

    @abstractmethod
    async def retrieve(
        self,
        *,
        query: str,
        top_k: int,
        tenant_id: str,
    ) -> list[RetrievedDocument]:
        """
        Retrieve the most relevant knowledge for a query.

        Args:
            query: User's natural language question.
            top_k: Maximum number of documents to return.
            tenant_id: Tenant whose knowledge base must be searched.

        Returns:
            Relevant document chunks.

        Raises:
            KnowledgeRetrievalError:
                If retrieval fails.
            NoRelevantDocumentsFound:
                If no relevant documents are found.
        """
        raise NotImplementedError


class KnowledgeRetriever(Retriever):
    """
    Default retriever implementation.

    Coordinates the embedding provider and vector store.
    """

    def __init__(
        self,
        *,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int,
        tenant_id: str,
    ) -> list[RetrievedDocument]:
        """
        Convert the query into an embedding and search the
        tenant's knowledge base.
        """

        if not query.strip():
            raise KnowledgeRetrievalError(
                "Knowledge query cannot be empty."
            )

        if not tenant_id.strip():
            raise KnowledgeRetrievalError(
                "Tenant ID is required for knowledge retrieval."
            )

        try:
            query_embedding = await self.embedding_provider.embed_text(
                query
            )

            raw_results = await self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                tenant_id=tenant_id,
            )

        except Exception as exc:
            raise KnowledgeRetrievalError(
                "Failed to retrieve knowledge documents."
            ) from exc

        if not raw_results:
            raise NoRelevantDocumentsFound(
                "No relevant documents were found."
            )

        return [
            RetrievedDocument(**result)
            for result in raw_results
        ]