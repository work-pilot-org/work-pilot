"""
Google Gemini LLM provider.

Contains only provider-specific communication with Google's Gemini API.
Tool execution and business logic are handled outside this layer.
"""

from __future__ import annotations

from typing import Any

from google import genai
from google.genai import errors, types

from shared_infrastructure.core.config import settings
from core.logger import get_logger
from infrastructure.providers.base_provider import BaseLLMProvider
from infrastructure.providers.exceptions import (
    GeminiRateLimitError,
    GeminiQuotaExhaustedError,
)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

logger = get_logger(__name__)


def is_transient_rate_limit(exc: Exception) -> bool:
    if not isinstance(exc, errors.APIError) or exc.code != 429:
        return False
    # Check if there's a retryDelay under 60 seconds (typically RPM limit)
    # If the delay is missing or large, it's likely a daily quota exhaustion
    try:
        details = getattr(exc, "details", []) or []
        if isinstance(details, dict) and "error" in details:
            details = details["error"].get("details", [])
            
        for d in details:
            if isinstance(d, dict) and d.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
                delay_str = d.get("retryDelay", "0s")
                delay = int(delay_str.replace("s", ""))
                if delay <= 60:
                    return True
    except Exception:
        pass
    
    # If no explicitly short retryDelay was found, don't blindly retry 
    # to avoid burning through Tenacity attempts on a hard daily limit.
    return False


class GeminiProvider(BaseLLMProvider):
    """Google Gemini implementation of BaseLLMProvider."""

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.gemini_api_key,
        )
        self._model = settings.gemini_model

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((errors.APIError, GeminiRateLimitError)),
        reraise=True,
    )
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
            error_details = getattr(exc, "details", None) or str(exc)
            
            if exc.code == 429:
                if is_transient_rate_limit(exc):
                    # Tenacity should catch this since we added the retry decorator. 
                    # If we reach here, it means Tenacity exhausted its attempts.
                    logger.error("Gemini API transient rate limit exhausted after retries", error=str(exc))
                    raise GeminiRateLimitError(f"Gemini API rate limit exceeded: {error_details}") from exc
                else:
                    logger.error("Gemini API daily quota exhausted", error=str(exc))
                    raise GeminiQuotaExhaustedError(f"Gemini API quota exhausted: {error_details}") from exc

            logger.error(
                "Gemini API request failed",
                status_code=exc.code,
                error=str(exc),
            )
            raise RuntimeError(
                f"Gemini API request failed: {exc.code} - {error_details}"
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

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((errors.APIError, GeminiRateLimitError)),
        reraise=True,
    )
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
            error_details = getattr(exc, "details", None) or str(exc)
            
            if exc.code == 429:
                if is_transient_rate_limit(exc):
                    # Tenacity should catch this if it's transient, but if retries exhausted:
                    logger.error("Gemini API transient rate limit for tools exhausted after retries", error=str(exc))
                    raise GeminiRateLimitError(f"Gemini API rate limit exceeded: {error_details}") from exc
                else:
                    logger.error("Gemini API daily quota for tools exhausted", error=str(exc))
                    raise GeminiQuotaExhaustedError(f"Gemini API quota exhausted: {error_details}") from exc

            logger.error(
                "Gemini tool request failed",
                status_code=exc.code,
                error=str(exc),
            )
            raise RuntimeError(
                f"Gemini API tool request failed: {exc.code} - {error_details}"
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