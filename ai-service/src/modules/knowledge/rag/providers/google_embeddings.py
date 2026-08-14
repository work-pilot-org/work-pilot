"""
Google Gemini embedding provider.

Provides text embeddings for the Knowledge Agent using
Google's Gemini embedding model through LangChain.
"""

from __future__ import annotations

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from core.config import settings
from modules.knowledge.exceptions import EmbeddingError
from modules.knowledge.rag.embeddings import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Google Gemini implementation of the EmbeddingProvider.
    """

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise EmbeddingError(
                "GEMINI_API_KEY is not configured."
            )

        try:
            self._embeddings = GoogleGenerativeAIEmbeddings(
                model="gemini-embedding-001",
                google_api_key=settings.gemini_api_key,
            )

        except Exception as exc:
            raise EmbeddingError(
                "Failed to initialize Gemini embedding provider."
            ) from exc

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        if not text.strip():
            raise EmbeddingError(
                "Cannot generate an embedding for empty text."
            )

        try:
            return await self._embeddings.aembed_query(
                text
            )

        except Exception as exc:
            raise EmbeddingError(
                "Failed to generate text embedding."
            ) from exc

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise EmbeddingError(
                "Cannot generate embeddings for empty text."
            )

        try:
            return await self._embeddings.aembed_documents(
                texts
            )

        except Exception as exc:
            raise EmbeddingError(
                "Failed to generate document embeddings."
            ) from exc