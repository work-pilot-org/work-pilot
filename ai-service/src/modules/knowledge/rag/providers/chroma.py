"""
ChromaDB provider for the Knowledge Agent.

This module contains the concrete implementation of the
VectorStore abstraction using ChromaDB.
"""

from __future__ import annotations

from typing import Any

import chromadb

from modules.knowledge.exceptions import VectorStoreError
from modules.knowledge.rag.vector_store import VectorStore


class ChromaVectorStore(VectorStore):
    """
    ChromaDB implementation of the VectorStore interface.
    """

    def __init__(
        self,
        *,
        persist_directory: str = "./data/chroma",
        collection_name: str = "workpilot_knowledge",
    ) -> None:
        try:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
            )

            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "hnsw:space": "cosine",
                },
            )

        except Exception as exc:
            raise VectorStoreError(
                "Failed to initialize ChromaDB."
            ) from exc

    async def add_documents(
        self,
        documents: list[dict[str, Any]],
        tenant_id: str,
    ) -> None:
        """
        Store document chunks in ChromaDB.
        """

        if not tenant_id.strip():
            raise VectorStoreError(
                "Tenant ID is required."
            )

        if not documents:
            return

        try:
            ids: list[str] = []
            embeddings: list[list[float]] = []
            contents: list[str] = []
            metadatas: list[dict[str, Any]] = []

            for document in documents:
                document_id = str(document["document_id"])
                chunk_id = str(document["chunk_id"])

                metadata = dict(
                    document.get("metadata", {})
                )

                metadata["document_id"] = document_id
                metadata["tenant_id"] = tenant_id

                ids.append(chunk_id)
                embeddings.append(document["embedding"])
                contents.append(document["content"])
                metadatas.append(metadata)

            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas,
            )

        except Exception as exc:
            raise VectorStoreError(
                "Failed to add documents to ChromaDB."
            ) from exc

    async def search(
        self,
        query_embedding: list[float],
        top_k: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        """
        Search for relevant document chunks belonging
        to the requested tenant.
        """

        if not tenant_id.strip():
            raise VectorStoreError(
                "Tenant ID is required."
            )

        if top_k <= 0:
            raise VectorStoreError(
                "top_k must be greater than zero."
            )

        try:
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={
                    "tenant_id": tenant_id,
                },
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )

            documents = result.get("documents", [[]])[0]
            distances = result.get("distances", [[]])[0]
            metadatas = result.get("metadatas", [[]])[0]

            results: list[dict[str, Any]] = []

            for content, distance, metadata in zip(
                documents,
                distances,
                metadatas,
            ):
                metadata = metadata or {}

                results.append(
                    {
                        "document_id": str(
                            metadata.get(
                                "document_id",
                                "",
                            )
                        ),
                        "content": content,
                        "score": 1.0 - float(distance),
                        "source": str(
                            metadata.get(
                                "source",
                                "unknown",
                            )
                        ),
                        "metadata": metadata,
                    }
                )

            return results

        except Exception as exc:
            raise VectorStoreError(
                "Failed to search ChromaDB."
            ) from exc

    async def delete_document(
        self,
        document_id: str,
        tenant_id: str,
    ) -> None:
        """
        Delete all chunks belonging to a document
        within the specified tenant.
        """

        if not tenant_id.strip():
            raise VectorStoreError(
                "Tenant ID is required."
            )

        try:
            self.collection.delete(
                where={
                    "$and": [
                        {
                            "tenant_id": tenant_id,
                        },
                        {
                            "document_id": document_id,
                        },
                    ],
                },
            )

        except Exception as exc:
            raise VectorStoreError(
                "Failed to delete document from ChromaDB."
            ) from exc

    async def document_exists(
        self,
        document_id: str,
        tenant_id: str,
    ) -> bool:
        """
        Check whether a document exists for a tenant.
        """

        if not tenant_id.strip():
            raise VectorStoreError(
                "Tenant ID is required."
            )

        try:
            result = self.collection.get(
                where={
                    "$and": [
                        {
                            "tenant_id": tenant_id,
                        },
                        {
                            "document_id": document_id,
                        },
                    ],
                },
                limit=1,
            )

            return bool(result.get("ids"))

        except Exception as exc:
            raise VectorStoreError(
                "Failed to check document existence."
            ) from exc