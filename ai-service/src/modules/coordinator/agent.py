"""
Coordinator Agent.

This module defines the central CoordinatorAgent class.
It acts as the primary orchestrator that receives a request from the API 
(via the service layer) and passes it through the Intent Detector, Planner, 
and Tool Executor, strictly avoiding any business logic execution itself.
"""

from typing import Any

from shared_infrastructure.core.config import settings
from core.logger import get_logger
from modules.coordinator.intent_detector import intent_detector
from modules.coordinator.registry import agent_registry
from modules.coordinator.response_builder import response_builder
from modules.coordinator.exceptions import CoordinatorError, UnknownDomainError
from modules.coordinator.constants import AgentDomain
from infrastructure.providers.exceptions import GeminiRateLimitError, GeminiQuotaExhaustedError


logger = get_logger(__name__)


class CoordinatorAgent:
    """
    The central orchestrator for the multi-agent AI system.
    """

    async def process(
        self, 
        user_message: str, 
        headers: dict[str, str] | None = None,
        user_context: dict | None = None
    ) -> Any:
        """
        Executes the full AI orchestration pipeline.
        
        Args:
            user_message (str): The raw request from the user.
            headers (dict | None): Trusted downstream headers (e.g., auth tokens).
            
        Returns:
            Any: The final unified response built by the response builder.
        """

        logger.info(
            "Processing user request",
            message=user_message,
        )

        # # Ask Gemini to determine which tool should be used.
        # tool_name = await gemini_client.generate(user_message)

        # tool_name = tool_name.strip()

        # logger.info(
        #     "Gemini selected tool",
        #     tool_name=tool_name,
        # )

        # # Temporary implementation:
        # # Route everything to the IT Agent.
        # return await get_it_agent().run(
        #     message=user_message,
        #     headers=headers,
        # )
        logger.info("Coordinator Agent pipeline started")
        
        if user_context:
            user_id = user_context.get("sub") or user_context.get("employee_id", "Unknown")
            system_note = f"\n\n[SYSTEM NOTE: You are currently talking to user ID: {user_id}. If a tool requires an employee_id or user_id, automatically use this ID unless specified otherwise.]"
            user_message += system_note
        try:
            # 1. Intent Detection (Figures out Domain and Intent)
            intent_classification = await intent_detector.detect_intent(user_message)
            
            # Short-circuit conversational intents
            if intent_classification.domain == AgentDomain.GENERAL.value:
                intent_upper = intent_classification.intent.upper()
                if intent_upper in ["GREETING", "HI", "HELLO"]:
                    return "Hello! I'm your WorkPilot AI assistant. How can I help you today?"
                elif intent_upper in ["THANKS", "THANK_YOU", "GRATITUDE", "THANKYOU"]:
                    return "You're welcome! Let me know if you need anything else."
                
                # Fallback for other general conversation
                from infrastructure.llm.gemini_client import gemini_client
                fallback_response = await gemini_client.generate(f"You are a helpful AI assistant for the WorkPilot HR and IT platform. The user just said: {user_message}\n\nPlease respond nicely and concisely.")
                return fallback_response

            # Early fail for truly unknown/unsupported actionable domains
            if intent_classification.domain == AgentDomain.UNKNOWN.value:
                raise UnknownDomainError(intent_classification.domain)
            
            # 2. Direct Specialist Agent Routing
            # Skip the Orchestration Planner and Tool Executor loop to save 2 Gemini API calls per request
            # Specialist agents (e.g. HR, IT) natively return a final natural language response.
            specialist_agent = agent_registry.get_agent(intent_classification.domain)
            
            logger.info("Routing request directly to specialist agent", domain=intent_classification.domain)
            
            final_response = await specialist_agent.run(
                message=user_message,
                headers=headers
            )
            
            logger.info("Coordinator Agent pipeline finished successfully")
            return final_response
            
        except (GeminiRateLimitError, GeminiQuotaExhaustedError) as e:
            logger.error("Coordinator Agent hit quota limits", error=str(e))
            raise e
        except Exception as e:
            logger.error("Coordinator Agent pipeline failed", error=str(e), exc_info=True)
            # 5. Handle Failures Gracefully
            error_msg = response_builder.build_error_response(error=e)
            raise CoordinatorError(error_msg) from e


# Singleton instance of the agent to be consumed by the API/Service layers
coordinator_agent = CoordinatorAgent()
