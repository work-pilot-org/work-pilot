"""
Vector store abstraction for the Knowledge Agent.

The RAG layer should not be tightly coupled to a specific
vector database such as ChromaDB, Qdrant, or Pinecone.

This module defines the interface that vector store
implementations must follow.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    """
    Abstract interface for vector store operations.
    """

    @abstractmethod
    async def add_documents(
        self,
        documents: list[dict[str, Any]],
        tenant_id: str,
    ) -> None:
        """
        Add document chunks to the vector store.

        Args:
            documents: Document chunks with their embeddings and metadata.
            tenant_id: Tenant that owns these documents.
        """
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        query_embedding: list[float],
        top_k: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        """
        Search for documents using a query embedding.

        Args:
            query_embedding: Vector representation of the query.
            top_k: Maximum number of results to return.
            tenant_id: Tenant whose knowledge base must be searched.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_document(
        self,
        document_id: str,
        tenant_id: str,
    ) -> None:
        """
        Delete all chunks belonging to a document.
        """
        raise NotImplementedError

    @abstractmethod
    async def document_exists(
    self,
    document_id: str,
    tenant_id: str,
) -> bool:
        """
Check whether a document has already been indexed
for a specific tenant.

Args:
    document_id: Unique document identifier.
    tenant_id: Tenant that owns the document.

Returns:
    True if the document exists for the tenant.
"""
        raise NotImplementedError