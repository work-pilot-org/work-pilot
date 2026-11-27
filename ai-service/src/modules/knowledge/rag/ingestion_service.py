"""
Knowledge document ingestion service.

Coordinates document extraction, chunking, embedding generation,
and vector-store persistence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from modules.knowledge.constants import (
    MAX_DOCUMENTS_PER_INGESTION,
    SUPPORTED_DOCUMENT_TYPES,
)
from modules.knowledge.exceptions import (
    IngestionError,
    UnsupportedFileTypeError,
)
from modules.knowledge.rag.embeddings import EmbeddingProvider
from modules.knowledge.rag.ingestion import DocumentIngestor
from modules.knowledge.rag.vector_store import VectorStore


class KnowledgeIngestionService:
    """
    Orchestrates the complete document ingestion pipeline.

    Flow:

        raw document
            ↓
        document ingestor
            ↓
        text chunks
            ↓
        embedding provider
            ↓
        embeddings
            ↓
        vector store
    """

    def __init__(
        self,
        *,
        ingestors: dict[str, DocumentIngestor],
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._ingestors = ingestors
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    async def ingest_document(
        self,
        *,
        document_id: str,
        content: bytes,
        filename: str,
        tenant_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Ingest a single document into the tenant's knowledge base.

        Args:
            document_id:
                Unique identifier for the source document.

            content:
                Raw document bytes.

            filename:
                Original filename.

            tenant_id:
                Tenant that owns the document.

            metadata:
                Additional document metadata.
        """

        if not document_id.strip():
            raise IngestionError(
                "Document ID is required."
            )

        if not tenant_id.strip():
            raise IngestionError(
                "Tenant ID is required."
            )

        if not content:
            raise IngestionError(
                "Document content cannot be empty."
            )

        extension = Path(filename).suffix.lower()

        if extension not in SUPPORTED_DOCUMENT_TYPES:
            raise UnsupportedFileTypeError(
                f"Unsupported document type: {extension}"
            )

        ingestor = self._ingestors.get(extension)

        if ingestor is None:
            raise UnsupportedFileTypeError(
                f"No ingestion provider configured for: {extension}"
            )

        try:
            ingestion_result = await ingestor.ingest(
                document_id=document_id,
                content=content,
                filename=filename,
                metadata=metadata,
            )

            if not ingestion_result.chunks:
                raise IngestionError(
                    "Document did not produce any searchable chunks."
                )

            embeddings = (
                await self._embedding_provider.embed_documents(
                    ingestion_result.chunks
                )
            )

            if len(embeddings) != len(
                ingestion_result.chunks
            ):
                raise IngestionError(
                    "Embedding count does not match chunk count."
                )

            documents: list[dict[str, Any]] = []

            for index, (chunk, embedding) in enumerate(
                zip(
                    ingestion_result.chunks,
                    embeddings,
                )
            ):
                documents.append(
                    {
                        "document_id": document_id,
                        "chunk_id": (
                            f"{document_id}:chunk:{index}"
                        ),
                        "content": chunk,
                        "embedding": embedding,
                        "metadata": {
                            **ingestion_result.metadata,
                            "chunk_index": index,
                        },
                    }
                )

            await self._vector_store.add_documents(
                documents=documents,
                tenant_id=tenant_id,
            )

        except (
            IngestionError,
            UnsupportedFileTypeError,
        ):
            raise

        except Exception as exc:
            raise IngestionError(
                f"Failed to ingest document: {filename}"
            ) from exc

    async def ingest_documents(
        self,
        *,
        documents: list[dict[str, Any]],
        tenant_id: str,
    ) -> None:
        """
        Ingest multiple documents for a tenant.

        Each document dictionary must contain:

            document_id
            content
            filename

        Optional:

            metadata
        """

        if not tenant_id.strip():
            raise IngestionError(
                "Tenant ID is required."
            )

        if not documents:
            return

        if len(documents) > MAX_DOCUMENTS_PER_INGESTION:
            raise IngestionError(
                "Maximum number of documents per ingestion "
                f"is {MAX_DOCUMENTS_PER_INGESTION}."
            )

        for document in documents:
            await self.ingest_document(
                document_id=str(
                    document["document_id"]
                ),
                content=document["content"],
                filename=str(
                    document["filename"]
                ),
                tenant_id=tenant_id,
                metadata=document.get("metadata"),
            )