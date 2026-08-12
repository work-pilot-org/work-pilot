"""
Intent Detector for the Coordinator Agent.

This module analyzes the user's natural language request and classifies it 
into a strict business domain and intent, using the LLM.
"""

from pydantic import BaseModel, Field

from core.logger import get_logger
from modules.coordinator.client import coordinator_llm_client
from modules.coordinator.constants import SUPPORTED_DOMAINS
from modules.coordinator.exceptions import IntentDetectionError, UnknownDomainError
from infrastructure.providers.exceptions import GeminiRateLimitError, GeminiQuotaExhaustedError
from modules.coordinator.prompts import build_intent_detection_prompt


logger = get_logger(__name__)


class IntentClassification(BaseModel):
    """
    Data model representing the structured classification of the user's request.
    Using Pydantic guarantees strong typing throughout the pipeline.
    """
    domain: str = Field(..., description="The target specialist domain (e.g., 'hr', 'it').")
    intent: str = Field(..., description="The concise intent string (e.g., 'CREATE_EMPLOYEE').")


class IntentDetector:
    """
    Analyzes incoming user requests to determine the correct routing domain and intent.
    """

    async def detect_intent(self, user_message: str) -> IntentClassification:
        """
        Calls the LLM to classify the user's message.
        
        Args:
            user_message (str): The raw natural language input from the user.
            
        Returns:
            IntentClassification: The strongly-typed classification result.
            
        Raises:
            IntentDetectionError: If the LLM fails or returns unparseable output.
            UnknownDomainError: If the LLM returns an unsupported domain.
        """
        logger.info("Starting intent detection", user_message_length=len(user_message))
        
        # Inject the active domains from constants.py into the prompt
        prompt = build_intent_detection_prompt(
            supported_domains=list(SUPPORTED_DOMAINS),
            user_message=user_message,
        )
        
        try:
            # We rely on the CoordinatorLLMClient to enforce JSON parsing
            raw_result = await coordinator_llm_client.generate_structured_json(prompt)
            classification = IntentClassification(**raw_result)
            
        except (GeminiRateLimitError, GeminiQuotaExhaustedError) as e:
            raise e
        except Exception as e:
            logger.error("Intent detection parsing failed", error=str(e))
            raise IntentDetectionError(f"Failed to classify intent: {str(e)}") from e
            
        # Validate that the LLM didn't hallucinate a non-existent domain
        # (Unless it explicitly classified it as 'unknown' due to ambiguity)
        if classification.domain != "unknown" and classification.domain not in SUPPORTED_DOMAINS:
            logger.warning(
                "LLM hallucinated unsupported domain", 
                hallucinated_domain=classification.domain
            )
            raise UnknownDomainError(classification.domain)
            
        logger.info(
            "Intent successfully detected",
            domain=classification.domain,
            intent=classification.intent
        )
        
        return classification


# Singleton instance for the coordinator module
intent_detector = IntentDetector()
