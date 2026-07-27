"""
Google Gemini LLM provider.

Contains only provider-specific communication with Google's Gemini API.
Tool execution and business logic are handled outside this layer.
"""

from __future__ import annotations

from typing import Any

from google import genai
from google.genai import errors, types

from core.config import settings
from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider

logger = get_logger(__name__)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini implementation of BaseLLMProvider."""

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.gemini_api_key,
        )
        self._model = settings.gemini_model

    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
    ) -> str:
        """Generate a plain text response."""

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
        )

        logger.info(
            "Sending request to Gemini",
            model=self._model,
        )

        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents=prompt,
                config=config,
            )

        except errors.APIError as exc:
            logger.error(
                "Gemini API request failed",
                status_code=exc.code,
                error=str(exc),
            )
            raise RuntimeError(
                "Gemini API request failed."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Unexpected Gemini provider error",
                error=str(exc),
            )
            raise RuntimeError(
                "Unexpected error while communicating with Gemini."
            ) from exc

        if not response.text:
            logger.warning(
                "Gemini returned an empty text response",
                model=self._model,
            )
            return ""

        logger.info(
            "Gemini response received",
            model=self._model,
        )

        return response.text

    async def generate_with_tools(
        self,
        contents: Any,
        *,
        tools: list[Any],
        system_instruction: str | None = None,
    ) -> Any:
        """
        Generate a response with manual function calling enabled.

        Gemini may request functions, but this provider never executes
        those functions itself.
        """

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True,
            ),
        )

        logger.info(
            "Sending tool-enabled request to Gemini",
            model=self._model,
            tool_count=len(tools),
        )

        try:
            response = await self._client.aio.models.generate_content(
                model=self._model,
                contents=contents,
                config=config,
            )

        except errors.APIError as exc:
            logger.error(
                "Gemini tool request failed",
                status_code=exc.code,
                error=str(exc),
            )
            raise RuntimeError(
                "Gemini API tool request failed."
            ) from exc

        except Exception as exc:
            logger.exception(
                "Unexpected Gemini tool request error",
                error=str(exc),
            )
            raise RuntimeError(
                "Unexpected error while communicating with Gemini."
            ) from exc

        logger.info(
            "Gemini tool response received",
            model=self._model,
            function_call_count=len(response.function_calls or []),
        )

        return response