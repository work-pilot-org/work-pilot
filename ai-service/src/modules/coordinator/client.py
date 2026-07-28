# Gemini router client (optional)
"""
Coordinator LLM Client.

This client wraps the global infrastructure Gemini client to provide
orchestration-specific helper methods (e.g., forced JSON parsing)
without duplicating the core SDK initialization.
"""

import json
from typing import Any

from infrastructure.llm.gemini_client import gemini_client
from modules.coordinator.exceptions import CoordinatorError


class CoordinatorLLMClient:
    """
    Provides orchestration-specific LLM operations by wrapping the global Gemini client.
    """

    async def generate_structured_json(self, prompt: str) -> dict[str, Any]:
        """
        Calls the LLM and parses the output as JSON.
        This is critical for the Intent Detector and Planner, which require 
        structured data rather than raw text.
        """
        try:
            # Strict Reuse: Calls the existing infrastructure client
            raw_response = await gemini_client.generate(prompt=prompt)
            
            # Clean up potential markdown formatting from the LLM output
            cleaned_response = self._strip_markdown_blocks(raw_response)
            
            return json.loads(cleaned_response)
            
        except json.JSONDecodeError as e:
            # Raises our custom orchestration exception for graceful handling
            raise CoordinatorError(f"Failed to parse structured JSON from LLM response: {str(e)}")
        except Exception as e:
            raise CoordinatorError(f"LLM generation failed during orchestration: {str(e)}")

    def _strip_markdown_blocks(self, text: str) -> str:
        """Helper to strip ```json and ``` markdown blocks commonly returned by Gemini."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()


# Singleton instance for the coordinator module
coordinator_llm_client = CoordinatorLLMClient()
