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
from modules.coordinator.planner import orchestration_planner
from modules.coordinator.tool_executor import tool_executor
from modules.coordinator.response_builder import response_builder


logger = get_logger(__name__)


class CoordinatorAgent:
    """
    The central orchestrator for the multi-agent AI system.
    """

    async def process(
        self, 
        user_message: str, 
        headers: dict[str, str] | None = None
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
        logger.info("Coordinator Agent pipeline started")
        
        try:
            # 1. Intent Detection (Figures out Domain and Intent)
            intent_classification = await intent_detector.detect_intent(user_message)
            
            # 2. Planning (Breaks the intent down into logical steps)
            execution_plan = await orchestration_planner.generate_plan(
                user_message=user_message, 
                intent_classification=intent_classification
            )
            
            # 3. Tool Execution (Routes to and invokes Specialist Agents)
            execution_results = await tool_executor.execute_plan(
                domain=intent_classification.domain,
                plan=execution_plan,
                user_message=user_message,
                headers=headers
            )
            
            # 4. Response Building (Summarizes the outcome)
            final_response = await response_builder.build_success_response(
                user_message=user_message,
                execution_results=execution_results
            )
            
            logger.info("Coordinator Agent pipeline finished successfully")
            return final_response
            
        except Exception as e:
            logger.error("Coordinator Agent pipeline failed", error=str(e), exc_info=True)
            # 5. Handle Failures Gracefully
            return response_builder.build_error_response(error=e)


# Singleton instance of the agent to be consumed by the API/Service layers
coordinator_agent = CoordinatorAgent()
