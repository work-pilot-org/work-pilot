"""
PDF document ingestion provider.

Responsible for extracting text from PDF documents and
converting the extracted text into searchable chunks.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from pypdf import PdfReader

from modules.knowledge.exceptions import (
    IngestionError,
    UnsupportedFileTypeError,
)
from modules.knowledge.rag.ingestion import (
    DocumentIngestionResult,
    DocumentIngestor,
    TextChunker,
)


class PdfDocumentIngestor(DocumentIngestor):
    """
    PDF implementation of the DocumentIngestor interface.
    """

    SUPPORTED_EXTENSION = ".pdf"

    def __init__(
        self,
        *,
        chunker: TextChunker | None = None,
    ) -> None:
        self._chunker = chunker or TextChunker()

    async def ingest(
        self,
        *,
        document_id: str,
        content: bytes,
        filename: str,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentIngestionResult:
        """
        Extract text from a PDF and split it into chunks.
        """

        if not document_id.strip():
            raise IngestionError(
                "Document ID is required."
            )

        if not content:
            raise IngestionError(
                "Document content cannot be empty."
            )

        if not filename.lower().endswith(
            self.SUPPORTED_EXTENSION
        ):
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {filename}"
            )

        try:
            reader = PdfReader(BytesIO(content))

            if not reader.pages:
                raise IngestionError(
                    "PDF does not contain any pages."
                )

            pages: list[str] = []

            for page in reader.pages:
                text = page.extract_text()

                if text and text.strip():
                    pages.append(text.strip())

            extracted_text = "\n\n".join(pages)

            if not extracted_text.strip():
                raise IngestionError(
                    "No extractable text was found in the PDF."
                )

            chunks = self._chunker.split(
                extracted_text
            )

            return DocumentIngestionResult(
                document_id=document_id,
                chunks=chunks,
                metadata={
                    **(metadata or {}),
                    "source": filename,
                    "filename": filename,
                    "document_type": "pdf",
                },
            )

        except (
            IngestionError,
            UnsupportedFileTypeError,
        ):
            raise

        except Exception as exc:
            raise IngestionError(
                f"Failed to ingest PDF: {filename}"
            ) from exc