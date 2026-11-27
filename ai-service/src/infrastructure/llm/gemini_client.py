"""
Gemini client for AI Service.
"""

from __future__ import annotations

from google import genai

from shared_infrastructure.core.config import settings


class GeminiClient:
    """
    Wrapper around the Google Gemini SDK.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self.model = settings.gemini_model

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from Gemini.
        """

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text


gemini_client = GeminiClient()