"""
Embedding abstraction for the Knowledge Agent.

This module defines the contract that all embedding
providers must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Abstract interface for generating text embeddings.
    """

    @abstractmethod
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError