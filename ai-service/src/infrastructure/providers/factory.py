"""
LLM provider factory.

Creates the configured LLM provider without exposing
provider-specific implementations to the application layer.
"""

from __future__ import annotations

from core.config import settings
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.gemini_provider import GeminiProvider


class LLMProviderFactory:
    """
    Factory responsible for creating LLM provider instances.
    """

    @staticmethod
    def create(provider: str | None = None) -> BaseLLMProvider:
        """
        Create an LLM provider.

        If no provider is explicitly supplied, the configured
        application provider is used.
        """

        provider_name = provider or settings.llm_provider

        match provider_name.lower():
            case "gemini":
                return GeminiProvider()

            case _:
                raise ValueError(
                    f"Unsupported LLM provider: {provider_name}"
                )


def get_llm_provider() -> BaseLLMProvider:
    """
    Return the configured LLM provider.
    """

    return LLMProviderFactory.create()