"""
Document ingestion for the Knowledge Agent.

The ingestion layer is responsible for converting source
documents into searchable text chunks.

Flow:

Document
    ↓
Text extraction
    ↓
Chunking
    ↓
Document chunks
    ↓
Embedding
    ↓
Vector Store
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from modules.knowledge.constants import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
)
from modules.knowledge.exceptions import IngestionError


class DocumentIngestionResult:
    """
    Represents the output produced by document ingestion.
    """

    def __init__(
        self,
        *,
        document_id: str,
        chunks: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.document_id = document_id
        self.chunks = chunks
        self.metadata = metadata or {}


class DocumentIngestor(ABC):
    """
    Abstract interface for document ingestion.

    Concrete implementations can support PDF, DOCX, TXT,
    or other document formats.
    """

    @abstractmethod
    async def ingest(
        self,
        *,
        document_id: str,
        content: bytes,
        filename: str,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentIngestionResult:
        """
        Process a document and return searchable chunks.

        Args:
            document_id: Unique identifier of the document.
            content: Raw document bytes.
            filename: Original document filename.
            metadata: Additional document metadata.

        Returns:
            DocumentIngestionResult containing the extracted
            and chunked text.

        Raises:
            IngestionError: If document processing fails.
        """
        raise NotImplementedError


class TextChunker:
    """
    Splits extracted document text into searchable chunks.

    RecursiveCharacterTextSplitter attempts to preserve
    meaningful sections of text while respecting the
    configured chunk size and overlap.
    """

    def __init__(
        self,
        *,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(
        self,
        text: str,
    ) -> list[str]:
        """
        Split extracted document text into searchable chunks.

        Args:
            text: Extracted document text.

        Returns:
            A list of cleaned text chunks.

        Raises:
            IngestionError: If the document contains no usable text.
        """

        if not text or not text.strip():
            raise IngestionError(
                "Cannot create chunks from empty document content."
            )

        chunks = self._splitter.split_text(text)

        if not chunks:
            raise IngestionError(
                "Document did not produce any text chunks."
            )

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]