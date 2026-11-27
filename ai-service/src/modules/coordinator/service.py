"""
Coordinator Service.

This module acts as the Application Service (Facade) for the Coordinator.
It orchestrates the Intent Detector, Planner, Tool Executor, and Response Builder
into a single, unified execution pipeline.
"""

from core.logger import get_logger

from modules.coordinator.intent_detector import intent_detector
from modules.coordinator.planner import orchestration_planner
from modules.coordinator.tool_executor import tool_executor
from modules.coordinator.response_builder import response_builder


logger = get_logger(__name__)


class CoordinatorService:
    """
    Main entry point for orchestration. Implements the core execution pipeline.
    """

    async def process_request(
        self, 
        user_message: str, 
        headers: dict[str, str] | None = None
    ) -> str:
        """
        Executes the full orchestration pipeline:
        Intent Detection -> Planning -> Execution -> Response Building
        
        Args:
            user_message (str): The raw natural language input from the user.
            headers (dict | None): Trusted downstream headers from the API.
            
        Returns:
            str: The final, human-readable response string for the API.
        """
        logger.info("Coordinator pipeline started")
        
        try:
            # Step 1: Detect Intent and Target Domain
            intent_classification = await intent_detector.detect_intent(user_message)
            
            # Step 2: Build the multi-step Execution Plan
            execution_plan = await orchestration_planner.generate_plan(
                user_message=user_message, 
                intent_classification=intent_classification
            )
            
            # Step 3: Execute the Plan via Specialist Agents (Routing & Tool Execution)
            execution_results = await tool_executor.execute_plan(
                domain=intent_classification.domain,
                plan=execution_plan,
                headers=headers
            )
            
            # Step 4: Build a Unified Natural Language Response
            final_response = await response_builder.build_success_response(
                user_message=user_message,
                execution_results=execution_results
            )
            
            logger.info("Coordinator pipeline finished successfully")
            return final_response
            
        except Exception as e:
            # We log the full traceback internally for debugging
            logger.error("Coordinator pipeline failed", error=str(e), exc_info=True)
            
            # Step 5: Handle Failures Gracefully
            # Safely mask the error into a polite string for the user
            return response_builder.build_error_response(error=e)


# FastAPI dependency injection factory used by router.py
def get_coordinator_service() -> CoordinatorService:
    """Returns a new instance of the Coordinator Service."""
    return CoordinatorService()
