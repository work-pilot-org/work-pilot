import asyncio
from pathlib import Path

from modules.knowledge.rag.providers.pdf_ingestion import (
    PdfDocumentIngestor,
)


async def main() -> None:
    pdf_path = Path(
        "test-data/workpilot_knowledge_test.pdf"
    )

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Test PDF not found: {pdf_path}"
        )

    content = pdf_path.read_bytes()

    ingestor = PdfDocumentIngestor()

    result = await ingestor.ingest(
        document_id="test-document-001",
        content=content,
        filename=pdf_path.name,
        metadata={
            "document_type": "policy",
            "test": True,
        },
    )

    print("PDF ingestion successful")
    print("========================")
    print("Document ID:", result.document_id)
    print("Number of chunks:", len(result.chunks))
    print("Metadata:", result.metadata)

    print("\nExtracted chunks:")
    print("=================")

    for index, chunk in enumerate(result.chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())